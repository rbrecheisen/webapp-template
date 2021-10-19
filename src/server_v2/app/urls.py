from django.urls import path, include
from . import views, api


urlpatterns = [
    path('login/', views.handle_login),
    path('', views.index),
    path('api/', api.index),
]
