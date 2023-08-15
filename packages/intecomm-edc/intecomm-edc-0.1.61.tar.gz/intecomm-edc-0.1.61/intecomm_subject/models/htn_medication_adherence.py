from edc_adherence.model_mixins import MedicationAdherenceModelMixin
from edc_model.models import BaseUuidModel

from ..model_mixins import CrfModelMixin


class HtnMedicationAdherence(
    MedicationAdherenceModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    condition_label = "Hypertension"

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Medication Adherence (Hypertension)"
        verbose_name_plural = "Medication Adherence (Hypertension)"
