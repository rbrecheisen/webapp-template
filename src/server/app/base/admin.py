from django.contrib import admin
from .models import DataSetModel, FileModel, TaskModel, TaskResultModel


@admin.register(DataSetModel)
class DataSetModelAdmin(admin.ModelAdmin):
    pass


@admin.register(FileModel)
class FileModelAdmin(admin.ModelAdmin):
    pass


@admin.register(TaskModel)
class TaskModelAdmin(admin.ModelAdmin):
    pass


@admin.register(TaskResultModel)
class TaskResultModelAdmin(admin.ModelAdmin):
    pass
