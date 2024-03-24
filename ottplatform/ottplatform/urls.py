# ottplatform/urls.py
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include  # Import the necessary view


admin.site.site_header = "OTT PLATFORM"



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ottapp.urls')),
  # Include ottapp URLs under /ottapp/
    # Add other app-specific URLs here
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
