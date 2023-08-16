"""
Models
"""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter
from allianceauth.groupmanagement.models import AuthGroup


class General(models.Model):
    """
    General module permissions
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta Definitions
        """

        verbose_name = "Fleet Finder"
        managed = False
        default_permissions = ()
        permissions = (
            ("access_fleetfinder", "Can access the Fleet Finder app"),
            ("manage_fleets", "Can manage fleets"),
        )


class Fleet(models.Model):
    """
    Fleet Model
    """

    class EsiError(models.TextChoices):
        """
        Choices for SRP Status
        """

        NOT_IN_FLEET = "NOT_IN_FLEET", _(
            "FC is not in the registered fleet anymore or fleet is no longer available."
        )
        NO_FLEET = "NO_FLEET", _("Registered fleet seems to be no longer available.")
        NOT_FLEETBOSS = "NOT_FLEETBOSS", _("FC is no longer the fleet boss.")
        FC_CHANGED_FLEET = "FC_CHANGED_FLEET", _("FC switched to another fleet.")

    fleet_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=50, default="", verbose_name=_("Fleet Name"))
    fleet_commander = models.ForeignKey(
        EveCharacter,
        on_delete=models.SET_NULL,
        related_name="fleetfinder_fleet_commander",
        default=None,
        null=True,
        blank=True,
        verbose_name=_("Fleet Commander"),
    )
    created_at = models.DateTimeField(verbose_name=_("Creation date and time"))
    motd = models.TextField(blank=True, default="", verbose_name=_("Fleet MOTD"))
    is_free_move = models.BooleanField(verbose_name=_("Free move"))

    groups = models.ManyToManyField(
        AuthGroup,
        related_name="fleetfinder_restricted_groups",
        help_text="Groups listed here will be able to join the fleet",
        verbose_name=_("Group restrictions"),
    )

    last_esi_error = models.CharField(
        max_length=16,
        blank=True,
        default="",
        choices=EsiError.choices,
        verbose_name=_("Last ESI error"),
    )

    last_esi_error_time = models.DateTimeField(
        null=True, blank=True, default=None, verbose_name=_("Last ESI error time")
    )

    esi_error_count = models.IntegerField(default=0, verbose_name=_("ESI error count"))

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta Definitions
        """

        default_permissions = ()
