from django.conf import settings
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AbstractUser(PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    """

    sso_id = models.CharField(
        _("SSO ID"),
        max_length=150,
        unique=True,
        error_messages={"unique": _("A user with that SSO ID already exists.")},
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = "sso_id"
    REQUIRED_FIELDS = []

    class Meta:
        abstract = True
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def __str__(self):
        return self.get_full_name() or self.email or self.sso_id

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True


class AbstractTeam(models.Model):
    name = models.CharField(max_length=250, unique=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True
        ordering = ["name"]
        verbose_name = _("team")
        verbose_name_plural = _("teams")

    def __str__(self):
        return self.name


class AbstractOrgGroup(models.Model):
    name = models.CharField(max_length=250, unique=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True
        ordering = ["name"]
        verbose_name = _("group")
        verbose_name_plural = _("groups")

    def __str__(self):
        return self.name
