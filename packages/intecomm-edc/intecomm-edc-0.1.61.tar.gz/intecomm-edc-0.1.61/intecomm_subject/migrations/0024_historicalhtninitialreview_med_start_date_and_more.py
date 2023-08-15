# Generated by Django 4.1.7 on 2023-04-04 12:54

from django.db import migrations, models
import edc_model.validators.date


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_subject", "0023_auto_20230404_0411"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalhtninitialreview",
            name="med_start_date",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="Medication start date, if known",
            ),
        ),
        migrations.AddField(
            model_name="htninitialreview",
            name="med_start_date",
            field=models.DateField(
                blank=True,
                null=True,
                validators=[edc_model.validators.date.date_not_future],
                verbose_name="Medication start date, if known",
            ),
        ),
    ]
