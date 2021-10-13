from django.urls import path, include
from .views import *


urlpatterns = [
    path('login/', handle_login),
    path('', datasets),
    path('datasets/', datasets),
    path('datasets/<str:dataset_id>', dataset),
    path('datasets/<str:dataset_id>/tasks/', tasks),
    path('tasks/', tasks),
    path('tasks/<str:task_id>', task),
    path('download/<str:dataset_id>', download),
    path('accounts/', include('django.contrib.auth.urls')),
]
