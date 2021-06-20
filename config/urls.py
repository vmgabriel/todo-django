"""config URL Configuration"""

# Libraries
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('todos/', include('todos.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
