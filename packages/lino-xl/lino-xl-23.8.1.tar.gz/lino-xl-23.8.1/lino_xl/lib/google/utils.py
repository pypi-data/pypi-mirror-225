# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import json
import requests
import datetime
from pathlib import Path
import logging
logger = logging.getLogger(__name__)

try:
    from google.oauth2.credentials import Credentials
    from google.auth.exceptions import RefreshError
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from httplib2.error import ServerNotFoundError
    from social_django.models import UserSocialAuth
except ImportError:
    class UserSocialAuth:
        pass

from django.conf import settings

from lino.api import dd

User = settings.SITE.user_model


def get_credentials(user: UserSocialAuth):

    with open(dd.plugins.google.client_secret_file) as f:
        client_secret = json.load(f)

    def get_expiry(creds_data):
        if creds_data['expiry']:
            return datetime.datetime.fromtimestamp(creds_data['expiry'])
        return datetime.datetime.fromtimestamp(
            creds_data['auth_time']) + datetime.timedelta(seconds=creds_data['expires_in'])

    creds = Credentials(
        token_uri=client_secret['web']['token_uri'],
        client_id=client_secret['web']['client_id'],
        client_secret=client_secret['web']['client_secret'],
        token=user.extra_data['access_token'],
        refresh_token=user.extra_data['refresh_token'],
        rapt_token=user.extra_data['rapt_token'],
        id_token=user.extra_data['id_token'],
        expiry=get_expiry(user.extra_data),
        scopes=scps.split() if isinstance(scps := user.extra_data['scopes'], str) else scps
    )

    if creds.expired:
        try:
            creds.refresh(Request())
            user.extra_data['access_token'] = creds.token
            user.extra_data['expiry'] = datetime.datetime.timestamp(creds.expiry)
            user.extra_data['refresh_token'] = creds.refresh_token
            user.extra_data['rapt_token'] = creds.rapt_token
            user.full_clean()
            user.save()
        except RefreshError as e:
            requests.post('https://oauth2.googleapis.com/revoke',
                params={'token': creds.token},
                headers={'content-type': 'application/x-www-form-urlencoded'}
            ).raise_for_status()
            logger.warning(f"{user.user}'s Token has been revoked, because of this:\n{e}\nNeeds re-authentication.")
            user.delete()

    return creds


def get_resource(user: User, people: bool = False):
    try:
        social_user = user.social_auth.get(provider='google')
    except UserSocialAuth.DoesNotExist:
        raise Exception(f"{user} does not have a connected google account")
    creds = get_credentials(social_user)
    if people:
        return build('people', 'v1', credentials=creds)
    return build('calendar', 'v3', credentials=creds)


def make_api_call(make_request_fn, args=tuple(), kwargs=None, msg_fn=None, silent=False, _retry=0):
    if kwargs is None:
        kwargs = {}
    try:
        return make_request_fn(*args, **kwargs).execute(num_retries=dd.plugins.google.num_retries)
    except HttpError as e:
        dd.logger.warning(e.reason)
        if msg_fn is not None:
            dd.logger.warning(msg_fn(e, *args, **kwargs))
        if e.status_code >= 500:
            # TODO: something wrong in the backend. Disable the related system tasks?
            pass
        if not silent:
            raise e
    except ServerNotFoundError as e:
        if _retry < dd.plugins.google.num_retries:
            return make_api_call(make_request_fn, args, kwargs, msg_fn, silent, _retry + 1)
        # TODO: disable the related system tasks?
        raise e
    return


def _get_resource(user: User, people: bool = False):
    """
    Do not use this in any production code.
    """
    try:
        user.social_auth.get(provider='google')
    except UserSocialAuth.DoesNotExist:
        try:
            import lino_book
        except ImportError:
            return None
        with (
                Path(lino_book.__file__).parent / 'projects' / 'noi1e' / 'tests' / 'demo_google_user.json'
        ).open('r') as f:
            user_data = json.load(f)
        social_user = UserSocialAuth(provider='google', user=user, **user_data)
        social_user.full_clean()
        social_user.save()
    return get_resource(user, people)
