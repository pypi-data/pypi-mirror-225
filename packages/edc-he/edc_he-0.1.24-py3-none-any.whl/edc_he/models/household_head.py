from django.conf import settings
from django.db import models
from edc_crf.model_mixins import (
    CrfModelMixin,
    CrfStatusModelMixin,
    SingletonCrfModelMixin,
)
from edc_model.models import BaseUuidModel

from ..model_mixins import HouseholdHeadModelMixin, HouseholdModelMixin


class HealthEconomicsHouseholdHead(
    SingletonCrfModelMixin,
    HouseholdHeadModelMixin,
    HouseholdModelMixin,
    CrfModelMixin,
    CrfStatusModelMixin,
    BaseUuidModel,
):
    subject_visit = models.OneToOneField(
        settings.SUBJECT_VISIT_MODEL,
        on_delete=models.PROTECT,
        related_name="he_hoh_subjectvisit",
    )

    # TODO: collapse hoh_ethnicity choices as per last revision (v3)

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Health Economics: Household head"
        verbose_name_plural = "Health Economics: Household head"
