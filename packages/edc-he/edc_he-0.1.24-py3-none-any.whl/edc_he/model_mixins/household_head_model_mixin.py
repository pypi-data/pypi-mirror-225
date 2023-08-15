from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import PROTECT
from edc_constants.choices import GENDER_NA, YES_NO
from edc_constants.constants import NOT_APPLICABLE, QUESTION_RETIRED
from edc_model_fields.fields import OtherCharField

from ..choices import EMPLOYMENT_STATUS_CHOICES, MARITAL_CHOICES, RELATIONSHIP_CHOICES


class HouseholdHeadModelMixin(models.Model):
    hoh = models.CharField(
        verbose_name="Are you the household head?",
        max_length=15,
        choices=YES_NO,
        help_text="If YES, STOP and save the form.",
    )

    hoh_gender = models.CharField(
        verbose_name="Is the household head female or male?",
        max_length=15,
        choices=GENDER_NA,
        default=NOT_APPLICABLE,
    )

    hoh_age = models.IntegerField(
        verbose_name="How old is the household head?",
        validators=[MinValueValidator(18), MaxValueValidator(110)],
        null=True,
        blank=True,
        help_text="In years as of today",
    )

    relationship_to_hoh = models.CharField(
        verbose_name="What is your relationship to the household head?",
        max_length=25,
        choices=RELATIONSHIP_CHOICES,
        default=NOT_APPLICABLE,
        help_text="Not applicable if patient is head of household",
    )

    relationship_to_hoh_other = OtherCharField(
        verbose_name="If OTHER relationship, specify ...",
    )

    hoh_religion = models.ForeignKey(
        "edc_he.Religions",
        verbose_name="How would you describe the household head’s religious orientation?",
        related_name="+",
        on_delete=PROTECT,
        null=True,
        blank=False,
        help_text="Not applicable if patient is head of household",
    )

    hoh_religion_other = OtherCharField(
        verbose_name="If OTHER religious orientation, specify ...",
    )

    hoh_ethnicity = models.ForeignKey(
        "edc_he.ethnicities",
        verbose_name="What is the household head’s ethnic background?",
        related_name="+",
        on_delete=PROTECT,
        null=True,
        blank=False,
        help_text="Not applicable if patient is head of household",
    )

    hoh_ethnicity_other = OtherCharField(
        verbose_name="If OTHER ethnic background, specify ...",
    )

    hoh_education = models.ForeignKey(
        "edc_he.education",
        verbose_name="Highest level of education completed by the household head?",
        related_name="+",
        on_delete=PROTECT,
        null=True,
        blank=False,
        help_text="Not applicable if patient is head of household",
    )

    hoh_education_other = OtherCharField(
        verbose_name="If OTHER education, specify ...",
    )

    hoh_employment_status = models.CharField(
        verbose_name="Household head’s employment status",
        max_length=25,
        choices=EMPLOYMENT_STATUS_CHOICES,
        default=NOT_APPLICABLE,
        help_text="Not applicable if patient is head of household",
    )

    hoh_employment_type = models.ForeignKey(
        "edc_he.employmenttype",
        verbose_name="Household head’s type of employment",
        related_name="+",
        on_delete=PROTECT,
        null=True,
        blank=False,
        help_text="Not applicable if patient is head of household",
    )

    hoh_employment_type_other = OtherCharField(
        verbose_name="If OTHER type of employment, specify ...",
        max_length=100,
    )

    hoh_marital_status = models.CharField(
        verbose_name="Household head’s marital status",
        max_length=25,
        choices=MARITAL_CHOICES,
        default=NOT_APPLICABLE,
        help_text="Not applicable if patient is head of household",
    )

    hoh_marital_status_other = OtherCharField(
        verbose_name="If OTHER marital status, specify ...",
    )

    hoh_insurance = models.ManyToManyField(
        "edc_he.insurancetypes",
        verbose_name="Household head’s health insurance and ‘club’ status ",
        related_name="+",
        help_text="Not applicable if patient is head of household",
    )

    hoh_insurance_other = OtherCharField(
        verbose_name="If OTHER, specify ...",
    )

    # not used
    hoh_religion_old = models.CharField(
        verbose_name="How would you describe the household head’s religious orientation?",
        max_length=25,
        default=QUESTION_RETIRED,
        editable=False,
    )

    # not used
    hoh_employment_type_old = models.CharField(
        verbose_name="Household head’s type of employment",
        max_length=25,
        default=QUESTION_RETIRED,
        editable=False,
    )

    # not used
    hoh_education_old = models.CharField(
        verbose_name="Highest level of education completed by the household head?",
        max_length=25,
        default=QUESTION_RETIRED,
        editable=False,
    )

    # not used
    hoh_ethnicity_old = models.CharField(
        verbose_name="What is the household head’s ethnic background?",
        max_length=25,
        default=QUESTION_RETIRED,
        editable=False,
    )

    class Meta:
        abstract = True
