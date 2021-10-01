import django_rq

from django.utils import timezone
from django.conf import settings

from .models import *
from .tasks import TaskUnknownError, TASK_REGISTRY


# DATASET MODEL

def get_dataset_models():
    return DataSetModel.objects.all()


def get_dataset_model(dataset_id):
    return DataSetModel.objects.get(pk=dataset_id)


def create_dataset_model(files, user):
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    ds = DataSetModel.objects.create(name='dataset-{}'.format(timestamp), owner=user)
    for f in files:
        FileModel.objects.create(file_obj=f, dataset=ds)
    return ds


def delete_dataset_model(dataset):
    dataset.delete()


# FILE MODEL

def get_file_models(dataset):
    return FileModel.objects.filter(dataset=dataset).all()


def get_file_model(file_id):
    return FileModel.objects.get(pk=file_id)


def delete_file_model(f):
    f.delete()


# TASK MODEL

def get_task_models_for_dataset(dataset):
    return TaskModel.objects.filter(dataset=dataset).all()


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
