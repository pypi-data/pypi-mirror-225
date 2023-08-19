# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from django.db import models
from django.utils import timezone

try:
    from googleapiclient.errors import HttpError
except:
    HttpError = Exception
from typing import NamedTuple

from lino.mixins import Modified
from lino.modlib.users.mixins import UserAuthored
from lino_xl.lib.cal.models import BaseSubscription
from lino.api import rt, dd, _

from .utils import get_resource, make_api_call
from .choicelists import AccessRoles, google_status
from .mixins import GoogleContactSynchronized


class CalendarSubscription(BaseSubscription, Modified):
    primary = dd.BooleanField(default=False)
    access_role = AccessRoles.field(default='owner')
    sync_token = dd.CharField(max_length=200, blank=True, null=True)
    """Used to retrieve only the changed entries from the remote server."""
    page_token = dd.CharField(max_length=200, blank=True, null=True)


dd.inject_field("users.User", "calendar_sync_token", dd.CharField(max_length=200, blank=True, null=True))
dd.inject_field("users.User", "calendar_page_token", dd.CharField(max_length=200, blank=True, null=True))


class DeletedEntry(dd.Model):
    class Meta:
        app_label = "google"
        abstract = dd.is_abstract_model(__name__, "DeletedEntry")

    calendar = dd.BooleanField(default=False)
    user = dd.ForeignKey('users.User', null=False, blank=False)
    event_id = dd.CharField(max_length=200, blank=True, null=True)
    calendar_id = dd.CharField(max_length=200)


class Contact(UserAuthored, GoogleContactSynchronized, Modified):
    allow_cascaded_delete = ["contact"]

    class Meta:
        app_label = "google"
        abstract = dd.is_abstract_model(__name__, "Contact")

    contact = dd.ForeignKey(dd.plugins.google.contacts_model)


class DeletedContact(UserAuthored):
    class Meta:
        app_label = "google"
        abstract = dd.is_abstract_model(__name__, "DeletedContact")

    contact_id = dd.CharField(max_length=200)


class ContactSyncToken(UserAuthored, Modified):
    class Meta:
        app_label = "google"
        abstract = dd.is_abstract_model(__name__, "ContactSyncToken")
        unique_together = ['user']

    sync_token = dd.CharField(max_length=300, null=True, blank=True)
    page_token = dd.CharField(max_length=300, null=True, blank=True)


class FailedEntries(NamedTuple):
    calendars = []
    events = []
    contacts = []


class Synchronizer:

    _failed_entries = None
    failed_entries = None
    user = None

    def __init__(self, user=None):
        if user is not None:
            self.setup(user)

    def setup(self, user):
        self.clear()
        self.user = user
        self.failed_entries = FailedEntries()

    def has_scope_contacts(self):
        return dd.plugins.google.has_scope('contact', self.user)

    def has_scope_calendar(self):
        return dd.plugins.google.has_scope('calendar', self.user)

    def pull_events(self, resource, sub, room):
        Event = rt.models.cal.Event

        def sync10(next_page_token=None):
            try:
                events = make_api_call(
                    lambda: resource.events().list(
                        calendarId=sub.calendar.google_id, maxResults=10,
                        syncToken=sub.sync_token, pageToken=next_page_token)
                )
                sub.sync_token = events.get('nextSyncToken') or sub.sync_token
            except HttpError:
                sub.page_token = next_page_token
                return

            if items := events['items']:
                for item in items:
                    Event.insert_or_update_google_event(item, room, self.user)

            if next_page_token := events.get('nextPageToken'):
                sync10(next_page_token)
            else:
                sub.page_token = None

        sync10(sub.page_token)
        sub.full_clean()
        sub.save()

    def sync_calendar(self):
        gcal = get_resource(self.user)

        Calendar = rt.models.cal.Calendar
        CalendarSubscription = rt.models.google.CalendarSubscription
        Event = rt.models.cal.Event

        # Outward sync

        if not settings.SITE.is_demo_site:
            cal_res = gcal.calendars()

            Calendar.sync_deleted_records()
            Event.sync_deleted_records()

            synched_cals = []

            for c in (qs := Calendar.get_outward_insert_update_queryset(self.user)):
                try:
                    c.insert_or_update_into_google(cal_res, self.user)
                    synched_cals.append(c.pk)
                except HttpError:
                    break

            if (qs := qs.exclude(pk__in=synched_cals)).count():
                self.failed_entries.calendars.append(qs)

            ers = gcal.events()
            e_failed = False
            for e in Event.get_outward_insert_update_queryset(self.user):
                if e_failed:
                    self.failed_entries.events.append(e)
                    continue
                try:
                    e.insert_or_update_into_google(ers, self.user)
                except HttpError:
                    e_failed = True

        # Inward sync

        def sync10(next_page_token=None):
            try:
                cals = make_api_call(
                    lambda: gcal.calendarList().list(
                        maxResults=10, syncToken=self.user.calendar_sync_token, showDeleted=True,
                        showHidden=True, pageToken=next_page_token
                    )
                )
            except HttpError:
                self.user.calendar_page_token = next_page_token
                return

            for cal in cals.get("items", []):
                if cal.get("deleted", False):
                    Calendar.delete_google_calendar(cal)
                    continue
                calendar, room = Calendar.insert_or_update_google_calendar(cal, self.user)

                try:
                    subscription = CalendarSubscription.objects.get(user=self.user, calendar=calendar)
                except CalendarSubscription.DoesNotExist:
                    subscription = CalendarSubscription(user=self.user, calendar=calendar)
                    ar = CalendarSubscription.get_default_table().request(user=self.user)
                    subscription.full_clean()
                    subscription.save_new_instance(ar)
                subscription.primary = cal.get("primary", False)
                subscription.access_role = cal.get("accessRole", "reader")
                subscription.full_clean()
                subscription.save()

                self.pull_events(gcal, subscription, room)

            if next_page_token := cals.get('nextPageToken'):
                sync10(next_page_token)
            else:
                self.user.calendar_page_token = None
                self.user.calendar_sync_token = cals.get('nextSyncToken')

        sync10(self.user.calendar_page_token)
        self.user.full_clean()
        self.user.save()

        gcal.close()

    def sync_contacts(self):
        Contact = rt.models.google.Contact

        token, __ = rt.models.google.ContactSyncToken.objects.get_or_create(user=self.user)
        people = rt.models.google.get_resource(self.user, True).people()

        if not settings.SITE.is_demo_site:
            Contact.sync_deleted_records()
            synched = []
            for c in (qs := Contact.get_outward_insert_update_queryset(self.user)):
                try:
                    c.insert_or_update_into_google(people)
                    synched.append(c.pk)
                except HttpError:
                    break

            if (qs := qs.exclude(pk__in=synched)).count():
                self.failed_entries.contacts.append(qs)

        def sync10():
            try:
                resp = make_api_call(lambda: people.connections().list(
                    resourceName="people/me",
                    personFields=Contact.person_fields,
                    pageToken=token.page_token,
                    syncToken=token.sync_token,
                    pageSize=10,
                    requestSyncToken=True
                ))
            except HttpError:
                return

            if "connections" not in resp:
                token.page_token = None
                token.sync_token = resp["nextSyncToken"]
                return resp

            for item in resp["connections"]:
                if (ks := len(item.keys())) == 2:
                    Contact.delete_google_contact(item, self.user)
                    continue
                assert ks > 2
                try:
                    Contact.insert_or_update_google_contact(item, self.user)
                except Exception as e:
                    dd.logger.exception(e)
                    token.full_clean()
                    token.save()
                    people.close()
                    raise e

            if pageToken := resp.get("nextPageToken"):
                token.page_token = pageToken
                sync10()
            else:
                token.page_token = None
                token.sync_token = resp["nextSyncToken"]

        sync10()

        token.full_clean()
        token.save()
        people.close()

    def __call__(self, cal_only=False, contacts_only=False):
        if not contacts_only:
            if self.has_scope_calendar():
                self.sync_calendar()
            else:
                dd.logger.info(f"{self.user} does not have the necessary scopes to sync Google calendar")

        if not cal_only:
            if self.has_scope_contacts():
                self.sync_contacts()
            else:
                dd.logger.info(f"{self.user} does not have the necessary scopes to sync Google contacts")

        for qs in (self.failed_entries.contacts + self.failed_entries.calendars):
            qs.update(modified=timezone.now())

        for event in self.failed_entries.events:
            event.full_clean()
            event.save()

        self._failed_entries = self.failed_entries
        self.failed_entries = None
        return self

    def clear(self):
        self._failed_entries = self.failed_entries = self.user = None

    def sync(self, cal_only=False, contacts_only=False):
        self(cal_only, contacts_only)
        self.failed_entries = FailedEntries()
        return self


class SynchronizeGoogle(dd.Action):
    help_text = _("Synchronize this database row with Google.")
    label = _("Sync Google")
    select_rows = True
    required_roles = dd.login_required()

    def run_from_ui(self, ar, **kwargs):
        if not ar.selected_rows:
            raise Exception
        for user in ar.selected_rows:
            Synchronizer(user)()
        ar.success()


dd.inject_action('users.User', synchronize_google=SynchronizeGoogle())

DELETED_EVENTS_META = {}
DELETED_CALENDARS_META = {}


@dd.receiver(dd.post_analyze)
def set_delete_signal_receivers(*args, **kwargs):
    @dd.receiver(dd.pre_delete, sender=rt.models.cal.Event)
    def event_will_get_deleted(sender, instance, **kw):
        if instance.google_id and instance.synchronize_with_google():
            sub = rt.models.google.CalendarSubscription.objects.filter(
                models.Q(access_role='writer') | models.Q(access_role='owner'),
                calendar=instance.get_calendar()
            ).first()
            if sub is not None and (user := sub.user) is not None:
                DELETED_EVENTS_META[instance.google_id] = user

    @dd.receiver(dd.post_delete, sender=rt.models.cal.Event)
    def event_deleted(sender, instance, **kw):
        if user := DELETED_EVENTS_META.get(instance.google_id):
            entry = rt.models.google.DeletedEntry(event_id=instance.google_id, user=user,
                                                  calendar_id=instance.get_calendar().google_id)
            entry.full_clean()
            entry.save()
            del DELETED_EVENTS_META[instance.google_id]

    @dd.receiver(dd.pre_delete, sender=rt.models.cal.Calendar)
    def calendar_will_get_deleted(sender, instance, **kw):
        if instance.google_id:
            sub = rt.models.google.CalendarSubscription.objects.filter(
                models.Q(access_role='writer') | models.Q(access_role='owner'),
                calendar=instance
            ).first()
            if sub is not None and (user := sub.user):
                DELETED_CALENDARS_META[instance.google_id] = user

    @dd.receiver(dd.post_delete, sender=rt.models.cal.Calendar)
    def calendar_deleted(sender, instance, **kw):
        if user := DELETED_CALENDARS_META.get(instance.google_id):
            entry = rt.models.google.DeletedEntry(calendar_id=instance.google_id, calendar=True, user=user)
            entry.full_clean()
            entry.save()
            del DELETED_CALENDARS_META[instance.google_id]

    @dd.receiver(dd.post_save, sender=dd.resolve_model(dd.plugins.google.contacts_model))
    def contact_modified(sender, instance, **kw):
        for obj in rt.models.google.Contact.objects.filter(contact=instance):
            obj.full_clean()
            obj.save()

    @dd.receiver(dd.post_delete, sender=rt.models.google.Contact)
    def contact_deleted(sender, instance, **kw):
        inst = rt.models.google.DeletedContact(user=instance.user, contact_id=instance.google_id)
        inst.save_new_instance(ar=inst.get_default_table().request(user=instance.user))
