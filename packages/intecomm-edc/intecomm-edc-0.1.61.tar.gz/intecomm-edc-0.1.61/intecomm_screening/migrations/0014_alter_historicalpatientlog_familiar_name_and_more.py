# Generated by Django 4.1.2 on 2022-11-30 02:07

import django.core.validators
from django.db import migrations
import django_crypto_fields.fields.encrypted_char_field


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_screening", "0013_alter_healthfacility_distance_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalpatientlog",
            name="familiar_name",
            field=django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                blank=True,
                help_text="Should be a name. Do NOT use MR, MRS, MISS, SIR, MADAM and other such titles. (Encryption: RSA local)",
                max_length=71,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Ensure name consists of letters only in upper case separated by single spaces",
                        regex="^(([A-Z]+ )*[A-Z]+)?$",
                    )
                ],
                verbose_name="By what NAME should we refer to you? (if we speak to you)",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="familiar_name",
            field=django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                blank=True,
                help_text="Should be a name. Do NOT use MR, MRS, MISS, SIR, MADAM and other such titles. (Encryption: RSA local)",
                max_length=71,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Ensure name consists of letters only in upper case separated by single spaces",
                        regex="^(([A-Z]+ )*[A-Z]+)?$",
                    )
                ],
                verbose_name="By what NAME should we refer to you? (if we speak to you)",
            ),
        ),
        migrations.AlterField(
            model_name="patientlog",
            name="familiar_name",
            field=django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                blank=True,
                help_text="Should be a name. Do NOT use MR, MRS, MISS, SIR, MADAM and other such titles. (Encryption: RSA local)",
                max_length=71,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Ensure name consists of letters only in upper case separated by single spaces",
                        regex="^(([A-Z]+ )*[A-Z]+)?$",
                    )
                ],
                verbose_name="By what NAME should we refer to you? (if we speak to you)",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="familiar_name",
            field=django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                blank=True,
                help_text="Should be a name. Do NOT use MR, MRS, MISS, SIR, MADAM and other such titles. (Encryption: RSA local)",
                max_length=71,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Ensure name consists of letters only in upper case separated by single spaces",
                        regex="^(([A-Z]+ )*[A-Z]+)?$",
                    )
                ],
                verbose_name="By what NAME should we refer to you? (if we speak to you)",
            ),
        ),
    ]
