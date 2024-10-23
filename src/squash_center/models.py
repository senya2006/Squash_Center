import uuid

from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import BaseModel, Player


class SquashCourt(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    is_operational = models.BooleanField(default=True)

    def __str__(self):
        return f"Court {self.name}"


class RentalEquipment(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    description = models.TextField()
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="media/equipment_images/", null=True, blank=True)

    def __str__(self):
        return self.name


class RentalRecord(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="rental_records")
    equipment = models.ForeignKey(RentalEquipment, on_delete=models.CASCADE, null=True, blank=True)
    court = models.ForeignKey(SquashCourt, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Checking that the court is working
        if not self.court.is_operational:
            raise ValidationError("Court is not operational")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Rental record for {self.user.get_full_name()} at {self.court.name}"
