from datetime import datetime, timedelta

from django.utils import timezone

from squash_center.models import RentalEquipment, RentalRecord, SquashCourt


def sample_court(name="Sample Court", is_operational=True):
    # Creates a sample squash court for testing.
    return SquashCourt.objects.create(
        name=name,
        is_operational=is_operational
    )


def sample_rental_equipment(name="Racket", description="Sample description", price_per_hour=5.00):
    # Creates a sample rental equipment for testing.
    return RentalEquipment.objects.create(
        name=name,
        description=description,
        price_per_hour=price_per_hour
    )


def sample_rental_record(user, court, equipment=None, start_time=None, end_time=None):
    # Creates a sample rental record for testing.
    if start_time is None:
        start_time = timezone.now()
    if end_time is None:
        end_time = start_time + timedelta(hours=1)

    return RentalRecord.objects.create(
        user=user,
        court=court,
        equipment=equipment,
        start_time=start_time,
        end_time=end_time
    )
