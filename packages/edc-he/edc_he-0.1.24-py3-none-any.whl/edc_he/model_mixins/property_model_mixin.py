from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO_DONT_KNOW_DWTA
from edc_constants.constants import NOT_APPLICABLE, QUESTION_RETIRED

from edc_he.choices import LAND_AREA_UNITS


class PropertyModelMixin(models.Model):
    land_owner = models.CharField(
        verbose_name="Do you own any land.",
        max_length=25,
        choices=YES_NO_DONT_KNOW_DWTA,
    )

    # QUESTION_RETIRED
    land_value_known = models.CharField(
        verbose_name="Do you know about how much is this worth in total?",
        max_length=25,
        default=QUESTION_RETIRED,
        help_text="Use cash equivalent in local currency",
    )

    land_value = models.IntegerField(
        verbose_name="About how much is this worth in total?",
        validators=[MinValueValidator(1), MaxValueValidator(999999999)],
        null=True,
        blank=True,
        help_text="Use cash equivalent in local currency",
    )

    land_surface_area = models.IntegerField(
        verbose_name="Surface area",
        validators=[MinValueValidator(1), MaxValueValidator(999999999)],
        null=True,
        blank=True,
    )

    land_surface_area_units = models.CharField(
        verbose_name="Surface area (units)",
        max_length=15,
        choices=LAND_AREA_UNITS,
        default=NOT_APPLICABLE,
        null=True,
        blank=True,
    )

    land_additional = models.CharField(
        verbose_name="Do you own any other property other than your primary dwelling?",
        max_length=25,
        choices=YES_NO_DONT_KNOW_DWTA,
    )

    # QUESTION_RETIRED
    land_additional_known = models.CharField(
        verbose_name="Do you know about how much is this worth in total?",
        max_length=25,
        default=QUESTION_RETIRED,
        help_text="Use cash equivalent in local currency",
    )

    land_additional_value = models.IntegerField(
        verbose_name="About how much is this worth in total?",
        validators=[MinValueValidator(1), MaxValueValidator(999999999)],
        null=True,
        blank=True,
        help_text="Use cash equivalent in local currency",
    )

    class Meta:
        abstract = True
