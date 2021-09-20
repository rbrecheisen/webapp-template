import os
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver


class DataSetModel(models.Model):
    name = models.CharField(max_length=1024, editable=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, editable=False, related_name='+', on_delete=models.CASCADE)


class FileModel(models.Model):
    file_obj = models.FileField(upload_to='')
    dataset = models.ForeignKey(DataSetModel, on_delete=models.CASCADE)


class TaskResultModel(models.Model):
    pass


class TaskModel(models.Model):
    name = models.CharField(max_length=1024, editable=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    job_id = models.CharField(max_length=128, null=True)
    dataset = models.ForeignKey(DataSetModel, on_delete=models.CASCADE)
    result = models.ForeignKey(TaskResultModel, null=True, on_delete=models.DO_NOTHING)


# Post-delete methods
@receiver(models.signals.post_delete, sender=DataSetModel)
def dataset_post_delete(sender, instance, **kwargs):
    pass


@receiver(models.signals.post_delete, sender=FileModel)
def image_post_delete(sender, instance, **kwargs):
    if instance.file_obj:
        if os.path.isfile(instance.file_obj.path):
            os.remove(instance.file_obj.path)


@receiver(models.signals.post_delete, sender=TaskResultModel)
def task_result_post_delete(sender, instance, **kwargs):
    pass


@receiver(models.signals.post_delete, sender=TaskModel)
def task_post_delete(sender, instance, **kwargs):
    pass
