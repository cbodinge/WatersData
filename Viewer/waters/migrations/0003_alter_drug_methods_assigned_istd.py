# Generated by Django 4.2.9 on 2024-01-08 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waters', '0002_remove_drugs_drug_name_remove_istds_istd_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drug_methods',
            name='assigned_istd',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='waters.istd_methods'),
        ),
    ]
