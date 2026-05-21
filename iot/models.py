import uuid
from django.db import models


class Device(models.Model):
    """
    Registry for IoT edge nodes deployed in fields.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_id = models.CharField(max_length=100, unique=True, help_text="Unique hardware identifier (e.g., MAC address or Node ID)")
    name = models.CharField(max_length=200, help_text="Human readable name of the device or field")
    location = models.CharField(max_length=255, blank=True, null=True, help_text="Physical location of the sensor")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.device_id})"


class SoilMoisture(models.Model):
    """
    Model to store soil moisture data with JSONB fields for flexible data storage.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='telemetry', null=True, blank=True)
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

class MotorState(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE, related_name='motor_state', null=True, blank=True)
    is_on = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        state = "ON" if self.is_on else "OFF"
        return f"{self.device.name if self.device else 'Global'} - {state}"
