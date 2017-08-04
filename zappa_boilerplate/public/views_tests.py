# -*- coding: utf-8 -*-
import mock

from zappa_boilerplate.test_utils import BaseTestCase


class TestViews(BaseTestCase):

    def test_status(self):
        expected = {'status': 'ok'}
        response = self.client.get('/status')
        self.assert200(response)
        self.assertEqual(response.json, expected)

    def test_about(self):
        response = self.client.get('/about')
        self.assert200(response)

    def test_home_get(self):
        response = self.client.get('/')
        self.assert200(response)

    def test_register_get(self):
        response = self.client.get('/register')
        self.assert200(response)

    @mock.patch("zappa_boilerplate.public.views.flash")  # mocks out the calls to flash in views.py
    @mock.patch("zappa_boilerplate.utils.flash")  # mocks out the calls to flash (errors) in utils.py
    def test_register_and_login(self, mock_flash_errors, mock_flash):
        username = 'foo'
        email = 'foo@example.com'
        password = 'foobar'

        register_form_data = {
            'username': username,
            'email': email,
            'password': password,
            'confirm': password
        }

        response = self.client.post('/register', data=register_form_data, follow_redirects=True)
        self.assert200(response)

        flash_calls = []
        login_form_data = {
            'username': username,
            'password': 'wrong_password'
        }

        response = self.client.post('/', data=login_form_data, follow_redirects=True)
        self.assert200(response)
        flash_calls.append(mock.call('Password - Invalid password', 'warning'))

        login_form_data = {
            'username': 'unknown_username',
            'password': password
        }

        response = self.client.post('/', data=login_form_data, follow_redirects=True)
        self.assert200(response)
        flash_calls.append(mock.call('Username - Unknown username', 'warning'))

        mock_flash_errors.assert_has_calls(flash_calls)

        login_form_data = {
            'username': username,
            'password': password
        }

        response = self.client.post('/', data=login_form_data, follow_redirects=True)
        self.assert200(response)
        mock_flash.assert_called_with('You are logged in.', 'success')

    @mock.patch("zappa_boilerplate.utils.flash")
    def test_login_form_validation_error(self, mock_flash):
        username = 'foo'

        form_data = {
            'username': username,
            # 'password': 'password', <-- leaving this out will cause a form validation error
        }

        response = self.client.post('/', data=form_data, follow_redirects=True)
        self.assert200(response)
        mock_flash.assert_called_with('Password - This field is required.', 'warning')

    @mock.patch("zappa_boilerplate.utils.flash")
    def test_register_error(self, mock_flash):
        username = 'foo'
        email = 'foo@example.com'
        password = 'foobar'

        form_data = {
            'username': username,
            'email': email,
            'password': password,
            # 'confirm': password <-- leaving this out will cause a form verification error
        }

        response = self.client.post('/register', data=form_data, follow_redirects=True)
        self.assert200(response)
        mock_flash.assert_called_with('Verify password - This field is required.', 'warning')

    @mock.patch("zappa_boilerplate.utils.flash")
    def test_register_username_twice(self, mock_flash):
        username = 'foo'
        email1 = 'foo1@example.com'
        email2 = 'foo2@example.com'
        password = 'foobar'

        form_data = {
            'username': username,
            'email': email1,
            'password': password,
            'confirm': password
        }

        response = self.client.post('/register', data=form_data, follow_redirects=True)
        self.assert200(response)

        form_data['email'] = email2
        response = self.client.post('/register', data=form_data, follow_redirects=True)
        self.assert200(response)
        mock_flash.assert_called_with('Username - Username already registered', 'warning')

    @mock.patch("zappa_boilerplate.utils.flash")
    def test_register_email_twice(self, mock_flash):
        username1 = 'foo1'
        username2 = 'foo2'
        email = 'foo@example.com'
        password = 'foobar'

        form_data = {
            'username': username1,
            'email': email,
            'password': password,
            'confirm': password
        }

        response = self.client.post('/register', data=form_data, follow_redirects=True)
        self.assert200(response)

        form_data['username'] = username2
        response = self.client.post('/register', data=form_data, follow_redirects=True)
        self.assert200(response)
        mock_flash.assert_called_with('Email - Email already registered', 'warning')

    def test_not_found_error(self):
        response = self.client.get('/invalid_url')
        self.assert404(response)

    def test_logout(self):
        email = 'foo@bar.com'
        username = 'foofoo'
        password = 'barbar'

        # register and login first
        register_form_data = {
            'username': username,
            'email': email,
            'password': password,
            'confirm': password
        }

        response = self.client.post('/register', data=register_form_data, follow_redirects=True)
        self.assert200(response)

        login_form_data = {
            'username': username,
            'password': password
        }

        # test that view redirects
        response = self.client.post('/', data=login_form_data, follow_redirects=True)
        self.assert200(response)

        response = self.client.get('/logout')
        self.assertStatus(response, 302)

        # login again and test that after redirection, returns 200
        response = self.client.post('/', data=login_form_data, follow_redirects=True)
        self.assert200(response)

        response = self.client.get('/logout', follow_redirects=True)
        self.assert200(response)

