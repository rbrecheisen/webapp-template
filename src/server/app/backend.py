import django_rq
import zipfile

from os.path import basename
from django.utils import timezone
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .models import *
from .tasks import TASK_REGISTRY
from .tasks.BaseTask import TaskUnknownError


# DATASET MODEL

def get_dataset_models():
    return DataSetModel.objects.all()


def get_dataset_model(dataset_id):
    return DataSetModel.objects.get(pk=dataset_id)


def create_dataset_model_from_files(files, user):
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    ds = DataSetModel.objects.create(name='dataset-{}'.format(timestamp), owner=user)
    for f in files:
        if isinstance(f, InMemoryUploadedFile) or isinstance(f, TemporaryUploadedFile):
            file_path = default_storage.save(f.name, ContentFile(f.read()))
            file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        else:
            file_path = f
        FilePathModel.objects.create(file_path=file_path, dataset=ds)
    return ds


def delete_dataset_model(dataset):
    dataset.delete()


def rename_dataset_model(dataset, new_name):
    dataset.name = new_name
    dataset.save()
    return dataset


# FILE PATH MODEL

def get_file_path_models(dataset):
    return FilePathModel.objects.filter(dataset=dataset).all()


def get_file_path_models_names(dataset):
    file_path_models = get_file_path_models(dataset)
    file_names = []
    for fp in file_path_models:
        file_names.append(os.path.split(fp.file_path)[1])
    return file_names


def get_file_path_model(file_path_id):
    return FilePathModel.objects.get(pk=file_path_id)


def delete_file_path_model(fp):
    fp.delete()


# TASK MODEL

def get_task_models_for_dataset(dataset):
    return TaskModel.objects.filter(dataset=dataset).all()


def get_task_models():
    return TaskModel.objects.all()


def get_task_model(task_id):
    return TaskModel.objects.get(pk=task_id)


# TASK TYPE

def get_task_types():
    return TASK_REGISTRY.keys()


# TASK

def create_task(task_type, dataset):
    if task_type in get_task_types():
        task_model = TaskModel.objects.create(name=task_type, dataset=dataset)
        q = django_rq.get_queue('default')
        job = q.enqueue(execute_task, task_model)
        task_model.job_id = job.id
        task_model.job_status = 'queued'
        task_model.save()
    else:
        raise TaskUnknownError()


@django_rq.job
def execute_task(task_model):
    task = TASK_REGISTRY[task_model.name]
    task.execute(task_model)


def cancel_and_delete_task(task_model):
    from redis import Redis
    from rq.exceptions import NoSuchJobError
    from django_rq.jobs import get_job_class
    try:
        # Try to cancel the job if it's still running
        redis = Redis(host=settings.RQ_QUEUES['default']['HOST'])
        cls = get_job_class()
        job = cls.fetch(task_model.job_id, connection=redis)
        job.cancel()
    except NoSuchJobError:
        pass
    task_model.delete()


def get_zipped_download(dataset):
    file_path = '/tmp/{}.zip'.format(dataset.name)
    with zipfile.ZipFile(file_path, 'w') as zip_obj:
        files = get_file_path_models(dataset)
        for f in files:
            fp = f.file_path
            zip_obj.write(fp, arcname=basename(fp))
    # Save ZIP file path in dataset so ZIP file is deleted when dataset is deleted
    dataset.zip_file_path = file_path
    dataset.save()
    return file_path
