from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import Client, TestCase

from squash_center.models import RentalRecord
from squash_center.utils.samples import sample_court, sample_rental_record


class TestSquashBooking(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a test user
        self.user = get_user_model().objects.create_user(email='player@example.com', password='password')
        # Create a test squash court
        self.court = sample_court(name="Court 1", is_operational=True)

    def test_single_user_booking(self):
        # Use the sample_rental_record function to create a lease record
        sample_rental_record(user=self.user, court=self.court)
        # Check that only 1 booking record was created
        self.assertEqual(RentalRecord.objects.count(), 1)

    def test_double_user_booking(self):
        # Create a second user
        user2 = get_user_model().objects.create_user(email='user2@example.com', password='password')
        # Create rental records for two users on the same court
        sample_rental_record(user=self.user, court=self.court)
        sample_rental_record(user=user2, court=self.court)
        # Check that 2 booking records were created
        self.assertEqual(RentalRecord.objects.count(), 2)

    def test_booking_court_not_operational(self):
        # Mark the court as not operational
        self.court.is_operational = False
        self.court.save()
        # Try to create a booking for a non-operational court and expect a ValidationError
        with self.assertRaises(ValidationError):
            sample_rental_record(user=self.user, court=self.court)
