from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import YES
from edc_metadata.metadata_rules import PredicateCollection

from ..utils import (
    get_assets_model_cls,
    get_household_head_model_cls,
    get_income_model_cls,
    get_patient_model_cls,
    get_property_model_cls,
)


class Predicates(PredicateCollection):
    app_label = "edc_he"
    visit_model = "edc_visit_tracking.subjectvisit"

    @staticmethod
    def get_household_head(visit):
        try:
            obj = get_household_head_model_cls().objects.get(
                subject_visit__subject_identifier=visit.subject_identifier
            )
        except ObjectDoesNotExist:
            obj = None
        return obj

    @staticmethod
    def household_head_required(visit, **kwargs) -> bool:
        return (
            not get_household_head_model_cls()
            .objects.filter(subject_visit__subject_identifier=visit.subject_identifier)
            .exists()
        )

    def patient_required(self, visit, **kwargs) -> bool:
        required = False
        if hoh_obj := self.get_household_head(visit):
            if (
                not get_patient_model_cls()
                .objects.filter(subject_visit__subject_identifier=visit.subject_identifier)
                .exists()
            ):
                required = hoh_obj.hoh == YES
        return required

    @staticmethod
    def assets_required(visit, **kwargs) -> bool:
        return (
            not get_assets_model_cls()
            .objects.filter(subject_visit__subject_identifier=visit.subject_identifier)
            .exists()
        )

    @staticmethod
    def property_required(visit, **kwargs) -> bool:
        return (
            not get_property_model_cls()
            .objects.filter(subject_visit__subject_identifier=visit.subject_identifier)
            .exists()
        )

    @staticmethod
    def income_required(visit, **kwargs) -> bool:
        return (
            not get_income_model_cls()
            .objects.filter(subject_visit__subject_identifier=visit.subject_identifier)
            .exists()
        )
