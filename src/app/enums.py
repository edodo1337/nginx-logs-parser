from django.db import models


class CollectionCommandRunStatus(models.TextChoices):
    IN_PROGRESS = "IN_PROGRESS", "IN_PROGRESS"
    FAILED = "FAILED", "FAILED"
    SUCCESS = "SUCCESS", "SUCCESS"
