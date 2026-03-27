from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from catalog import views

urlpatterns = [
    path("", include("catalog.urls")),
    path("admin/", admin.site.urls),
    path("catalog/", include("catalog.urls")),
    path("add-to-cart/<slug:slug>/", views.add_to_cart, name="add_to_cart"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
                          document_root=settings.MEDIA_ROOT)
    
