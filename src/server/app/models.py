import os

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver


class DataSetModel(models.Model):
    name = models.CharField(max_length=1024, editable=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # If user owning the dataset is deleted, also delete dataset
    owner = models.ForeignKey(
        User, editable=False, related_name='+', on_delete=models.CASCADE)


class FileModel(models.Model):
    file_obj = models.FileField(upload_to='')
    # If dataset gets deleted, delete its files
    dataset = models.ForeignKey(DataSetModel, on_delete=models.CASCADE)


class TaskModel(models.Model):
    name = models.CharField(max_length=1024, editable=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    job_id = models.CharField(max_length=128, null=True)
    job_status = models.CharField(max_length=16, null=True)
    # Delete task if dataset gets deleted
    dataset = models.ForeignKey(DataSetModel, on_delete=models.CASCADE)


@receiver(models.signals.post_delete, sender=FileModel)
def file_post_delete(sender, instance, **kwargs):
    if instance.file_obj:
        if os.path.isfile(instance.file_obj.path):
            os.remove(instance.file_obj.path)
