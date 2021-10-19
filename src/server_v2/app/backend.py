import os

from django.utils import timezone
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .models import DataSetModel, FilePathModel


def get_dataset_models(user):
    return DataSetModel.objects.filter(owner=user)


def get_dataset_model(dataset_id):
    return DataSetModel.objects.get(pk=dataset_id)


def create_dataset_model_from_files(files, user):
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    dataset = DataSetModel.objects.create(name='dataset-{}'.format(timestamp), owner=user)
    for f in files:
        if isinstance(f, InMemoryUploadedFile) or isinstance(f, TemporaryUploadedFile):
            file_path = default_storage.save(f.name, ContentFile(f.read()))
            file_path = os.path.join(settings.MEDIA_ROOT, file_path)
        else:
            file_path = f
        FilePathModel.objects.create(file_path=file_path, dataset=dataset)
    return dataset


def rename_dataset_model(dataset_id, new_name):
    dataset = get_dataset_model(dataset_id)
    dataset.name = new_name
    dataset.save()


def delete_dataset_model(dataset_id):
    dataset = get_dataset_model(dataset_id)
    dataset.delete()
