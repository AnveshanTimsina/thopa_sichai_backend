import logging
from rest_framework import serializers
from .models import SoilMoisture, Device

logger = logging.getLogger('iot')


class SoilMoistureSerializer(serializers.ModelSerializer):
    """
    Serializer for SoilMoisture model with proper validation.
    """
    ip_address = serializers.IPAddressField(
        required=True,
        error_messages={"invalid": "Invalid IP address format.", "required": "IP address is required."}
    )

    class Meta:
        model = SoilMoisture
        fields = ['id', 'device', 'data', 'metadata', 'ip_address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'device', 'created_at', 'updated_at']

    def validate_data(self, value):
        """
        Validate that data is a valid non-empty JSON object (dict).
        """
        if not isinstance(value, dict):
            logger.warning("Invalid data type: %s, expected dict", type(value))
            raise serializers.ValidationError("Data must be a valid JSON object.")
        if not value:
            logger.warning("Empty data object provided")
            raise serializers.ValidationError("Data cannot be empty.")
        return value

    def validate_metadata(self, value):
        """
        Validate that metadata is a valid JSON object (dict) if provided.
        """
        if value is not None and not isinstance(value, dict):
            logger.warning("Invalid metadata type: %s, expected dict", type(value))
            raise serializers.ValidationError("Metadata must be a valid JSON object or null.")
        return value

    def create(self, validated_data):
        """
        Create a new SoilMoisture instance.
        """
        ip_addr = validated_data.get('ip_address')
        logger.info("Creating new SoilMoisture record from IP: %s", ip_addr)
        
        metadata = validated_data.get('metadata', {}) or {}
        device_id = metadata.get('device_id')
        
        device_obj = None
        if device_id:
            device_obj, created = Device.objects.get_or_create(
                device_id=device_id,
                defaults={'name': f"Auto-Registered Node: {device_id}"}
            )
            validated_data['device'] = device_obj
            
        instance = super().create(validated_data)
        logger.info("Successfully created SoilMoisture record with ID: %s", instance.id)
        return instance

    def update(self, instance, validated_data):
        """
        Update a SoilMoisture instance.
        """
        logger.info("Updating SoilMoisture record with ID: %s", instance.id)
        instance = super().update(instance, validated_data)
        logger.info("Successfully updated SoilMoisture record with ID: %s", instance.id)
        return instance
