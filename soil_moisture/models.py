import uuid
from django.db import models


class SoilMoisture(models.Model):
    """
    Model to store soil moisture data with JSONB fields for flexible data storage.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = models.JSONField(help_text="Main data field for soil moisture information")
    metadata = models.JSONField(null=True, blank=True, help_text="Optional metadata field")
    ip_address = models.CharField(max_length=45, help_text="IP address of the data source")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'SoilMoisture'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['ip_address']),
        ]

    def __str__(self):
        return f"SoilMoisture {self.id} - {self.ip_address}"

