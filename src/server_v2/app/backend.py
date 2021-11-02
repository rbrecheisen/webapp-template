import os
import django_rq

from django.utils import timezone
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .models import DataSetModel, FilePathModel, TaskModel
from .tasks import TASK_REGISTRY


def get_dataset_models(user):
    return DataSetModel.objects.filter(owner=user)


def get_dataset_model(dataset_id):
    return DataSetModel.objects.get(pk=dataset_id)


def create_dataset_model_from_files(files, user):
    # TODO: create randomly named sub-directories for each dataset to avoid naming conflicts
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    dataset = DataSetModel.objects.create(name='dataset-{}'.format(timestamp), owner=user)
    for f in files:
        if isinstance(f, InMemoryUploadedFile) or isinstance(f, TemporaryUploadedFile):
            file_path = default_storage.save(f.name, ContentFile(f.read()))
            file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        else:
            file_path = f
        FilePathModel.objects.create(path=file_path, dataset=dataset)
    return dataset


def rename_dataset_model(dataset_id, new_name):
    dataset = get_dataset_model(dataset_id)
    dataset.name = new_name
    dataset.save()
    return dataset


def delete_dataset_model(dataset_id):
    dataset = get_dataset_model(dataset_id)
    dataset.delete()


def get_file_path_models(dataset_id):
    dataset = get_dataset_model(dataset_id)
    return FilePathModel.objects.filter(dataset=dataset).all()


def get_file_names(dataset_id):
    file_path_models = get_file_path_models(dataset_id)
    file_names = []
    for fp in file_path_models:
        file_names.append(os.path.split(fp.path)[1])
    return file_names


def get_task_classes():
    return TASK_REGISTRY.keys()


def get_task_models(dataset_id):
    dataset = get_dataset_model(dataset_id)
    return TaskModel.objects.filter(dataset=dataset).all()


def create_task_model(dataset, task_class):
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    task_model = TaskModel.objects.create(
        name='{}-{}'.format(task_class, timestamp), class_name=task_class, dataset=dataset)
    return task_model


def get_task_model(task_id):
    return TaskModel.objects.get(pk=task_id)


def get_task_class(task_id):
    task = get_task_model(task_id)
    task_class = TASK_REGISTRY[task.class_name]['class']
    return task_class


def get_task_form(task_id):
    task = get_task_model(task_id)
    task_form = TASK_REGISTRY[task.class_name]['form_class']()
    return task_form


def rename_task_model(task_id, new_name):
    task = get_task_model(task_id)
    task.name = new_name
    task.save()
    return task


def delete_task_model(task_id):
    task = get_task_model(task_id)
    task.delete()


def start_task_in_background(task_model):
    q = django_rq.get_queue('default')
    job = q.enqueue(start_task_job, task_model)
    task_model.job_id = job.id
    task_model.job_status = 'queued'
    task_model.save()
    return task_model


@django_rq.job
def start_task_job(task_model):
    task = get_task_class(task_model.id)()
    task.execute(task_model)
