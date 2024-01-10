# Generated by Django 4.0.4 on 2024-01-03 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='runs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run_name', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='samples',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_name', models.CharField(max_length=255)),
                ('sample_type', models.CharField(choices=[('CAL', 'Standard'), ('QC', 'Quality Control')], default='QC', max_length=4)),
                ('inj_time', models.DateTimeField(null=True)),
                ('active', models.BooleanField(default=True)),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waters.runs')),
            ],
        ),
        migrations.CreateModel(
            name='istds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('istd_name', models.CharField(max_length=255)),
                ('area', models.FloatField(null=True)),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waters.samples')),
            ],
        ),
        migrations.CreateModel(
            name='drugs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drug_name', models.CharField(max_length=255)),
                ('exp_conc', models.FloatField(null=True)),
                ('area', models.FloatField(null=True)),
                ('area2', models.FloatField(null=True)),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waters.samples')),
            ],
        ),
    ]