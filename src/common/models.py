from django.contrib.auth import get_user_model
from django.db import models


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    edit_by = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="edited_%(class)s_records", null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
