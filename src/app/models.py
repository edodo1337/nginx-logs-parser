from django.db import models

from app.enums import CollectionCommandRunStatus


class NginxLog(models.Model):
    """Model to store Nginx logs."""

    time = models.DateTimeField()
    remote_ip = models.GenericIPAddressField()
    remote_user = models.CharField(max_length=255, blank=True, default="")
    request = models.CharField(max_length=255)
    response = models.PositiveIntegerField()
    bytes = models.PositiveIntegerField()
    referrer = models.CharField(max_length=255, blank=True, default="")
    agent = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Nginx Log"
        verbose_name_plural = "Nginx logs"
        ordering = ["-time"]

    def __str__(self):
        return f"{self.remote_ip} - {self.time}"

    @classmethod
    def last_loaded_timestamp(cls):
        last_log = cls.objects.order_by("time").last()
        if last_log:
            return last_log.time
        return None


class CollectionCommandRun(models.Model):
    """Model to track the status of import_logs command runs."""

    filename = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=CollectionCommandRunStatus,
        default=CollectionCommandRunStatus.IN_PROGRESS,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    error = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.filename} - {self.get_status_display()}"

    def set_failed(self, error: str):
        self.status = CollectionCommandRunStatus.FAILED
        self.error = error
        self.save()

    def set_success(self):
        self.status = CollectionCommandRunStatus.SUCCESS
        self.save()
