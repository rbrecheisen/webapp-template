from rest_framework import serializers
from .models import DataSetModel, FilePathModel, TaskModel


class DataSetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSetModel
        fields = ('id', 'name', 'created', 'owner', 'zip_path', )


class FilePathModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilePathModel
        fields = ('id', 'path', )


class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = ('id', 'name', 'parameters', 'created', 'job_id', 'job_status', 'errors', 'info', )
