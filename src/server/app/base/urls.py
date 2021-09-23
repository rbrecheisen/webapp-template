from django.urls import path, include
from .views import *


urlpatterns = [
    path('login/', handle_login),
    path('', datasets),
    path('datasets/', datasets),
    path('datasets/<str:dataset_id>', dataset),
    path('tasks/', tasks),
    path('tasks/<str:task_id>', task),
    path('accounts/', include('django.contrib.auth.urls')),
]
