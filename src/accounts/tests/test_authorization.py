import unittest
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class TestAuthPlayer(TestCase):

    def setUp(self):
        # Setup method to initialize the test client and create two users:
        # a regular user (self.user) and a manager (self.manager) who has staff access.
        self.client = Client()
        self.user = get_user_model().objects.create_user(email='player@example.com', password='12345678')
        self.manager = get_user_model().objects.create_user(email='manager@example.com', password='12345678',
                                                            is_staff=True)

    def test_user_login_wrong_email(self):
        # Test if login fails with an incorrect email.
        user_login = self.client.login(email='wrong_email', password='12345678')
        self.assertFalse(user_login)

    def test_user_login_wrong_password(self):
        # Test if login fails with an incorrect password for a valid email.
        user_login = self.client.login(email='player@example.com', password='wrong_password')
        self.assertFalse(user_login)

    # User redirected, access denied
    def test_user_access_admin_panel(self):
        # Test if a regular user gets redirected when trying to access the admin panel.
        self.client.force_login(self.user)
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    # The manager has access
    def test_manager_access_admin_panel(self):
        # Test if a manager has access to the admin panel.
        self.client.force_login(self.manager)
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @unittest.skip("No court booking page implemented yet.")
    def test_user_access_booking_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('court_booking_page'))  # Example: page for booking a court
        self.assertEqual(response.status_code, HTTPStatus.OK)  # The user can see the page

    @unittest.skip("No court booking page implemented yet.")
    def test_unauthenticated_access_booking_page(self):
        # Unauthorized user is redirected to log in
        response = self.client.get(reverse('court_booking_page'))
        self.assertEqual(response.status_code,
                         HTTPStatus.FOUND)

    def test_deactivated_user_login(self):
        # A deactivated user cannot log in
        self.user.is_active = False
        self.user.save()
        user_login = self.client.login(email='player@example.com', password='12345678')
        self.assertFalse(user_login)

    @unittest.skip("We dont have index page, will have it in future")
    def test_manager_access_index_page(self):
        # Test if a regular user can access the index page.
        self.client.force_login(self.user)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @unittest.expectedFailure
    def test_manager_access_admin_panel_failure_expected(self):
        # Expected failure test: manager tries to access a page with an incorrect HTTP status.
        self.client.force_login(self.manager)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
