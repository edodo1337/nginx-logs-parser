from django.contrib import admin

from app.models import CollectionCommandRun, NginxLog


class NginxLogAdmin(admin.ModelAdmin):
    list_display = ("id", "time", "remote_ip", "agent")
    search_fields = ("id", "time", "remote_ip", "agent")
    list_filter = ("time",)
    ordering = ("-time",)


class CollectionCommandRunAdmin(admin.ModelAdmin):
    list_display = ("filename", "id", "status", "created_at")
    search_fields = ("id", "filename", "status")
    list_filter = ("status", "created_at")
    ordering = ("-created_at",)


admin.site.register(NginxLog, NginxLogAdmin)
admin.site.register(CollectionCommandRun, CollectionCommandRunAdmin)
