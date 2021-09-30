from django.contrib import admin
from .models import DataSetModel, FileModel, TaskModel


@admin.register(DataSetModel)
class DataSetModelAdmin(admin.ModelAdmin):
    pass


@admin.register(FileModel)
class FileModelAdmin(admin.ModelAdmin):
    pass


@admin.register(TaskModel)
class TaskModelAdmin(admin.ModelAdmin):
    pass
