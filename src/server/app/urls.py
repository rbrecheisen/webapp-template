from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.handle_login),
    path('', views.datasets),
    path('datasets/', views.datasets),
    path('datasets/<str:dataset_id>', views.dataset),
    path('accounts/', include('django.contrib.auth.urls')),
]
