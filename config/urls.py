"""config URL Configuration"""

# Libraries
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", include("pages.urls")),
    path("", include("pwa.urls")),
    path("admin/", admin.site.urls),

    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")),

    path("todos/", include("todos.urls")),
    path("socials/", include("socials.urls")),
    path("buys/", include("to_buy.urls")),
    path("products/", include("products.urls")),
    path("stores/", include("stores.urls")),
    path("cash_flows/", include("cash_flow.urls")),
    path("library/", include("library.urls")),
    path("home/", include("home.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
