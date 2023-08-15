from edc_adherence.model_mixins import MedicationAdherenceModelMixin
from edc_model.models import BaseUuidModel

from ..model_mixins import CrfModelMixin


class HivMedicationAdherence(
    MedicationAdherenceModelMixin,
    CrfModelMixin,
    BaseUuidModel,
):
    condition_label = "HIV"

    class Meta(CrfModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Medication Adherence (HIV)"
        verbose_name_plural = "Medication Adherence (HIV)"
