from django.db import models
from django.db.models import TextChoices


# Create your models here.

class runs(models.Model):
    run_name = models.CharField(max_length=255, null=False)
    active = models.BooleanField(default=True, null=False)


class samples(models.Model):
    class SampleTypes(TextChoices):
        CALIBRATION = 'CAL', 'Standard'
        QUALITY_CONTROL = 'QC', 'Quality Control'

    sample_name = models.CharField(max_length=255, null=False)
    sample_type = models.CharField(max_length=4, choices=SampleTypes.choices,
                                   default=SampleTypes.QUALITY_CONTROL, null=False)

    inj_time = models.DateTimeField(null=True)
    active = models.BooleanField(default=True, null=False)

    def __str__(self):
        return self.sample_name


class istd_methods(models.Model):
    run = models.ForeignKey(runs, on_delete=models.CASCADE)
    istd_name = models.CharField(max_length=255, null=False)


class drug_methods(models.Model):
    run = models.ForeignKey(runs, on_delete=models.CASCADE)
    drug_name = models.CharField(max_length=255, null=False)

    min = models.FloatField(null=True)
    max = models.FloatField(null=True)

    assigned_istd = models.ForeignKey(istd_methods, on_delete=models.DO_NOTHING, null=True)


class drugs(models.Model):
    sample = models.ForeignKey(samples, on_delete=models.CASCADE)
    method = models.ForeignKey(drug_methods, on_delete=models.CASCADE)

    exp_conc = models.FloatField(null=True)
    area = models.FloatField(null=True)
    area2 = models.FloatField(null=True)


class istds(models.Model):
    sample = models.ForeignKey(samples, on_delete=models.CASCADE)
    method = models.ForeignKey(istd_methods, on_delete=models.CASCADE)
    area = models.FloatField(null=True)
