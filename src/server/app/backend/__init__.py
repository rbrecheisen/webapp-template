from django.utils import timezone

from src.server.app.models import DataSetModel, FileModel


def get_datasets():
    return DataSetModel.objects.all()


def get_dataset(dataset_id):
    return DataSetModel.objects.get(pk=dataset_id)


def create_dataset(files, user):
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    ds = DataSetModel.objects.create(name='dataset-{}'.format(timestamp), owner=user)
    for f in files:
        FileModel.objects.create(file_obj=f, dataset=ds)
    return ds


def delete_dataset(dataset):
    dataset.delete()


def get_files(dataset):
    return FileModel.objects.filter(dataset=dataset).all()


def get_file(file_id):
    return FileModel.objects.get(pk=file_id)


def delete_file(f):
    f.delete()
