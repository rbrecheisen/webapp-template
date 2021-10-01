from django.contrib import admin
from .models import DataSetModel, FilePathModel, TaskModel


@admin.register(DataSetModel)
class DataSetModelAdmin(admin.ModelAdmin):
    pass


@admin.register(FilePathModel)
class FilePathModelAdmin(admin.ModelAdmin):
    pass


@admin.register(TaskModel)
class TaskModelAdmin(admin.ModelAdmin):
    pass
