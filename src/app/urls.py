from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from app.api import logs_router

api = NinjaAPI(title="Nginx Parser")
api.add_router("/logs/", logs_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
