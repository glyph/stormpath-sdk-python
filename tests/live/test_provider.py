""""
Integration tests for various pieces involved in external provider support.
"""

import json
from unittest import main
from os import getenv
from requests import Session
from tests.live.base import AuthenticatedLiveBase
from stormpath.error import Error as StormpathError
from stormpath.resources import Provider


class TestProviderDirectories(AuthenticatedLiveBase):

    def test_creating_provider_directory_passes_provider_info(self):
        directory = self.client.directories.create(
            {
                'name': self.get_random_name(),
                'description': 'Testing Google Auth Provider',
                'provider':
                    {
                        'client_id': 'some-client-id',
                        'client_secret': 'some-client-secret',
                        'redirect_uri': 'some-redirect-uri',
                        'provider_id': Provider.GOOGLE
                    }
            })

        app = self.client.applications.create(
            {
                'name': self.get_random_name(),
                'description': 'Testing app for Google Auth',
                'status': 'enabled'
            })

        self.client.account_store_mappings.create(
            {
                'application': app,
                'account_store': directory,
                'list_index': 0,
                'is_default_account_store': False,
                'is_default_group_store': False
            })

        with self.assertRaises(StormpathError) as se:
            app.get_provider_account(
                provider=Provider.GOOGLE, code='some-code')

        self.assertTrue("Google error message: 400 Bad Request" in str(
            se.exception.developer_message))

        directory.delete()
        app.delete()

    def test_get_provider_account_makes_request_to_facebook(self):
        facebook_api_key_id = getenv('FACEBOOK_API_KEY_ID')
        facebook_api_key_secret = getenv('FACEBOOK_API_KEY_SECRET')

        if not facebook_api_key_id:
            self.fail("Please set FACEBOOK_API_KEY_ID environment variable!")
        if not facebook_api_key_secret:
            self.fail(
                "Please set FACEBOOK_API_KEY_SECRET environment variable!")

        s = Session()
        res = s.request(
            'GET', 'https://graph.facebook.com/oauth/access_token',
            params={
                'client_id': facebook_api_key_id,
                'client_secret': facebook_api_key_secret,
                'grant_type': 'client_credentials'
            })
        access_token = res.text.split('=')[1]

        res = s.request(
            'GET',
            'https://graph.facebook.com/%s/accounts/test-users' % (
                facebook_api_key_id ),
            params={
                'installed': 'true',
                'name': 'Some User',
                'locale': 'en_US',
                'permissions': 'read_stream',
                'method': 'post',
                'access_token': access_token,
            })
        access_token = json.loads(res.text)['access_token']

        directory = self.client.directories.create(
            {
                'name': self.get_random_name(),
                'description': 'Testing Facebook Auth Provider',
                'provider':
                    {
                        'client_id': facebook_api_key_id,
                        'client_secret': facebook_api_key_secret,
                        'provider_id': Provider.FACEBOOK
                    }
            })

        app = self.client.applications.create(
            {
                'name': self.get_random_name(),
                'description': 'Testing app for Facebook Auth',
                'status': 'enabled'
            })

        self.client.account_store_mappings.create(
            {
                'application': app,
                'account_store': directory,
                'list_index': 0,
                'is_default_account_store': False,
                'is_default_group_store': False
            })

        with self.assertRaises(StormpathError) as se:
            app.get_provider_account(
                provider=Provider.FACEBOOK, access_token=access_token)

        self.assertTrue(
            "Stormpath is unable to create or update the account because the "
            "Facebook response did not contain the required 'email' "
            "property." in str(se.exception.developer_message))

        directory.delete()
        app.delete()

    def test_get_provider_account_makes_request_to_github(self):
        github_api_key_id = 'some-api-key-id'
        github_api_key_secret = 'some-api-secret'

        directory = self.client.directories.create(
            {
                'name': self.get_random_name(),
                'description': 'Testing Github Auth Provider',
                'provider':
                    {
                        'client_id': github_api_key_id,
                        'client_secret': github_api_key_secret,
                        'provider_id': Provider.GITHUB
                    }
            })

        app = self.client.applications.create(
            {
                'name': self.get_random_name(),
                'description': 'Testing app for Github Auth',
                'status': 'enabled'
            })

        self.client.account_store_mappings.create(
            {
                'application': app,
                'account_store': directory,
                'list_index': 0,
                'is_default_account_store': False,
                'is_default_group_store': False
            })

        with self.assertRaises(StormpathError) as se:
            app.get_provider_account(
                provider=Provider.GITHUB, access_token='some-access-token')

        self.assertTrue("Github error message: 401 Unauthorized" in str(
            se.exception.developer_message))

        directory.delete()
        app.delete()

    def test_get_provider_account_makes_request_to_linkedin(self):
        linkedin_api_key_id = 'some-api-key-id'
        linkedin_api_key_secret = 'some-api-key-secret'

        directory = self.client.directories.create(
            {
                'name': self.get_random_name(),
                'description': 'Testing LinkedIn Auth Provider',
                'provider':
                    {
                        'client_id': linkedin_api_key_id,
                        'client_secret': linkedin_api_key_secret,
                        'provider_id': Provider.LINKEDIN
                    }
            })

        app = self.client.applications.create(
            {
                'name': self.get_random_name(),
                'description': 'Testing app for LinkedIn Auth',
                'status': 'enabled'
            })

        self.client.account_store_mappings.create(
            {
                'application': app,
                'account_store': directory,
                'list_index': 0,
                'is_default_account_store': False,
                'is_default_group_store': False
            })

        with self.assertRaises(StormpathError) as se:
            app.get_provider_account(
                provider=Provider.LINKEDIN, access_token='some-access-token')

        self.assertTrue("Linkedin error message: Invalid access token." in str(
            se.exception.developer_message))

        directory.delete()
        app.delete()


if __name__ == '__main__':
    main()