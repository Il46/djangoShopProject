from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")),
    path("", include("catalog.urls")),
    path("my-orders/", include("orders.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
