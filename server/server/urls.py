from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_api/', include('user_api.urls')),
    path('file_api/', include('file_api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)