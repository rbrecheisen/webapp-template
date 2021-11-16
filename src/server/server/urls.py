from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('session_security/', include('session_security.urls')),
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('django-rq/', include('django_rq.urls')),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
