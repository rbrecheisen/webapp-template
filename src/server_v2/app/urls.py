from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views, api


urlpatterns = [
    path('', views.index),
    path('datasets/', views.get_datasets),
    path('datasets/create', views.create_dataset),
    path('datasets/<str:dataset_id>', views.get_dataset),
    path('datasets/<str:dataset_id>/rename', views.rename_dataset),
    path('datasets/<str:dataset_id>/delete', views.delete_dataset),
    path('login/', views.handle_login),
    path('api/tokens/', obtain_auth_token, name='tokens'),
    path('api/', api.index),
    path('api/datasets/', api.get_datasets),
    path('api/datasets/create', api.create_dataset),
    path('api/datasets/<str:dataset_id>', api.get_dataset),
    path('api/datasets/<str:dataset_id>/rename', api.rename_dataset),
    path('api/datasets/<str:dataset_id>/delete', api.delete_dataset),
    path('api/datasets/<str:dataset_id>/tasks/', api.get_tasks),
    path('api/datasets/<str:dataset_id>/tasks/create', api.create_task),
    path('api/tasks/<str:task_id>', api.get_task),
    path('api/tasks/<str:task_id>/start', api.start_task),
    path('api/tasks/<str:task_id>/delete', api.delete_task),
]
