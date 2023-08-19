# -*- coding: UTF-8 -*-
# Copyright 2008-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""This is Lino's module to make synchronization with Google's content.
See :doc:`/plugins/google`.

"""

import json
from pathlib import Path

from django.db.models import ObjectDoesNotExist
from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    verbose_name = _("Google API")
    # partner_model = 'google.Person'
    # extends_models = ['Person']

    needs_plugins = ['lino.modlib.users', 'lino_xl.lib.addresses', 'lino_xl.lib.phones']

    contacts_model = "contacts.Person"
    num_retries = 3

    sync_immediately = False
    """
    Not used yet.

    Syncs a database entry with google on `save`.
    """

    ## settings

    backend = 'lino_xl.lib.google.backend.LinoGoogleOAuth2'

    # default is set on on_init method.
    client_secret_file = None
    """The `path` to the GoogleAPI secret file."""

    scopes = [
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/contacts',
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/calendar.events'
    ]
    """ GoogleAPi Scopes

    After modifying these scopes, delete all database entry for this provider
    and reauthenticate.

    """
    application_name = "LinoOAuthClient"
    """ The Application's name defined in the google API Console"""

    entry_state_translation = (
        ('confirmed', ('confirmed',)),
        ('tentative', ('tentative',)),
        ('cancelled', ('cancelled',)),
    )

    guest_state_translation = (
        ('needsAction', ('needsAction',)),
        ('declined', ('decliend',)),
        ('tentative', ('tentative',)),
        ('accepted', ('accepted',)),
    )

    def on_init(self):
        super().on_init()
        if not self.site.has_feature('third_party_authentication'):
            return
        from lino.core.site import has_socialauth
        if has_socialauth:
            self.needs_plugins.append('social_django')
            if self.client_secret_file is None:
                self.client_secret_file = self.site.site_dir / "google_creds.json"
            if isinstance(self.client_secret_file, str):
                self.client_secret_file = Path(self.client_secret_file)
            if not self.client_secret_file.exists():
                raise Exception(
                    "Please make sure to provide OAuth client credentials\n"
                    "accessable from google. Look at the following link for help:\n"
                    "\thttps://support.google.com/cloud/answer/6158849?hl=en")
            with self.client_secret_file.open() as f:
                client_secret = json.load(f)
            self.site.update_settings(
                SOCIAL_AUTH_GOOGLE_KEY=client_secret['web']['client_id'],
                SOCIAL_AUTH_GOOGLE_SECRET=client_secret['web']['client_secret'],
                SOCIAL_AUTH_GOOGLE_SCOPE=self.scopes,
                SOCIAL_AUTH_GOOGLE_USE_UNIQUE_USER_ID=True,
                SOCIAL_AUTH_GOOGLE_AUTH_EXTRA_ARGUMENTS={
                    'access_type': 'offline',
                    'include_granted_scopes': 'true',
                    'prompt': 'select_account'
                },
                SOCIAL_AUTH_GOOGLE_PIPELINE=(
                    'social_core.pipeline.social_auth.social_details',
                    'social_core.pipeline.social_auth.social_uid',
                    'social_core.pipeline.social_auth.auth_allowed',
                    'social_core.pipeline.social_auth.social_user',
                    'social_core.pipeline.user.get_username',
                    # 'social_core.pipeline.mail.mail_validation',
                    # 'social_core.pipeline.social_auth.associate_by_email',
                    'social_core.pipeline.user.create_user',
                    'social_core.pipeline.social_auth.associate_user',
                    'lino_xl.lib.google.pipeline.intercept_extra_data',
                    'social_core.pipeline.social_auth.load_extra_data',
                    'social_core.pipeline.user.user_details',
                )
            )
            if not self.site.social_auth_backends:
                self.site.social_auth_backends = []
            self.site.social_auth_backends.append(self.backend)

    @staticmethod
    def has_scope(scope_type, user):
        """
        :param str scope_type: Should be either 'calendar' or 'contact'
        :return bool: Tells whether a certain type of scope is available for the user.
        """
        assert scope_type in ['calendar', 'contact']
        try:
            suser = user.social_auth.get(provider='google')
        except ObjectDoesNotExist:
            return False

        scopes_list = suser.extra_data["scopes"].split()

        if scope_type == "calendar":
            return ('https://www.googleapis.com/auth/calendar.events' in scopes_list
                    and 'https://www.googleapis.com/auth/calendar' in scopes_list)
        if scope_type == "contact":
            return 'https://www.googleapis.com/auth/contacts' in scopes_list

    def get_requirements(self, site):
        yield "social-auth-app-django"
        yield "google-api-python-client"
        yield "google-auth"
        yield "google-auth-httplib2"
        yield "google-auth-oauthlib"
