# Generated by Django 4.2.9 on 2024-01-08 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waters', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drugs',
            name='drug_name',
        ),
        migrations.RemoveField(
            model_name='istds',
            name='istd_name',
        ),
        migrations.RemoveField(
            model_name='samples',
            name='run',
        ),
        migrations.CreateModel(
            name='istd_methods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('istd_name', models.CharField(max_length=255)),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waters.runs')),
            ],
        ),
        migrations.CreateModel(
            name='drug_methods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drug_name', models.CharField(max_length=255)),
                ('min', models.FloatField(null=True)),
                ('max', models.FloatField(null=True)),
                ('assigned_istd', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='waters.istd_methods')),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waters.runs')),
            ],
        ),
        migrations.AddField(
            model_name='drugs',
            name='method',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='waters.drug_methods'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='istds',
            name='method',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='waters.istd_methods'),
            preserve_default=False,
        ),
    ]
