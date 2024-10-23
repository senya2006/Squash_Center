from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from accounts.managers import PlayerManager


class Player(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("name"), max_length=150, blank=True)
    last_name = models.CharField(_("surname"), max_length=150, blank=True)
    email = models.EmailField(
        _("email address"), unique=True, error_messages={"unique": _("A user with that email already exists.")}
    )
    phone_number = PhoneNumberField(
        unique=False,
        null=True,
        blank=True,
        error_messages={"unique": _("A user with that phone number already exists.")},
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    birthday = models.DateTimeField(_("birth date"), null=True, blank=True)
    photo = models.ImageField(_("photo"), upload_to="images/users_avatars", null=True, blank=True)

    objects = PlayerManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("player")
        verbose_name_plural = _("players")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def get_registration_duration(self):
        return f"Time on site: {timezone.now() - self.date_joined}"

    def __str__(self):
        return f"{self.get_full_name()} ({str(self.phone_number)})"


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    edit_by = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="edited_%(class)s_records", null=True, blank=True)

    # "edited_%(class)s_records" unique names

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
