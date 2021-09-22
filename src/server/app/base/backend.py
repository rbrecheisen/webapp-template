from django.utils import timezone

from .models import *


class Backend:

    @staticmethod
    def get_datasets():
        return DataSetModel.objects.all()

    @staticmethod
    def get_dataset(dataset_id):
        return DataSetModel.objects.get(pk=dataset_id)

    @staticmethod
    def create_dataset(files, user):
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        ds = DataSetModel.objects.create(name='dataset-{}'.format(timestamp), owner=user)
        for f in files:
            FileModel.objects.create(file_obj=f, dataset=ds)
        return ds

    @staticmethod
    def delete_dataset(dataset):
        dataset.delete()

    @staticmethod
    def get_files(dataset):
        return FileModel.objects.filter(dataset=dataset).all()

    @staticmethod
    def get_file(file_id):
        return FileModel.objects.get(pk=file_id)

    @staticmethod
    def delete_file(f):
        f.delete()

    @staticmethod
    def get_tasks(dataset):
        return TaskModel.objects.filter(dataset=dataset).all()
