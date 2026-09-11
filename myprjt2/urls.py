from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp2.urls')),
]

urlpatterns += [
    path(
        settings.MEDIA_URL.lstrip('/'),
        serve,
        {'document_root': settings.MEDIA_ROOT}
    ),
]