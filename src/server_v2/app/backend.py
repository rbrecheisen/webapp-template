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
    return FilePathModel.objects.filter(dataset=dataset)


def get_file_names(dataset_id):
    file_path_models = get_file_path_models(dataset_id)
    file_names = []
    for fp in file_path_models:
        file_names.append(os.path.split(fp.path)[1])
    return file_names
