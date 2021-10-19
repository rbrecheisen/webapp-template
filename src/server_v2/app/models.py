import os

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver


class DataSetModel(models.Model):

    name = models.CharField(max_length=1024, editable=True, null=False)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, editable=False, related_name='+', on_delete=models.CASCADE)
    zip_path = models.CharField(max_length=1024, null=True)


class FilePathModel(models.Model):

    path = models.CharField(max_length=2048, editable=True, null=False)
    dataset = models.ForeignKey(DataSetModel, on_delete=models.CASCADE)


class TaskModel(models.Model):

    name = models.CharField(max_length=1024, editable=True, null=False)
    parameters = models.JSONField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    job_id = models.CharField(max_length=128, null=True)
    job_status = models.CharField(max_length=16, null=True)
    errors = models.CharField(max_length=2048, null=True)
    info = models.CharField(max_length=2048, null=True)
    dataset = models.ForeignKey(DataSetModel, on_delete=models.CASCADE)


@receiver(models.signals.post_delete, sender=DataSetModel)
def dataset_post_delete(sender, instance, **kwargs):
    if instance.zip_path and os.path.isfile(instance.zip_path):
        os.remove(instance.zip_path)


@receiver(models.signals.post_delete, sender=FilePathModel)
def file_path_post_delete(sender, instance, **kwargs):
    if instance.path and os.path.isfile(instance.path):
        os.remove(instance.path)
