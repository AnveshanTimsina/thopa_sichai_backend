import logging
from rest_framework import serializers
from .models import SoilMoisture
import ipaddress

logger = logging.getLogger('soil_moisture')


class SoilMoistureSerializer(serializers.ModelSerializer):
    """
    Serializer for SoilMoisture model with proper validation.
    """
    class Meta:
        model = SoilMoisture
        fields = ['id', 'data', 'metadata', 'ip_address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_data(self, value):
        """
        Validate that data is a valid JSON object (dict).
        """
        if not isinstance(value, dict):
            logger.warning(f"Invalid data type: {type(value)}, expected dict")
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
            logger.warning(f"Invalid metadata type: {type(value)}, expected dict")
            raise serializers.ValidationError("Metadata must be a valid JSON object or null.")
        return value

    def validate_ip_address(self, value):
        """
        Validate IP address format (supports both IPv4 and IPv6).
        """
        if not value:
            raise serializers.ValidationError("IP address is required.")
        
        try:
            ipaddress.ip_address(value)
        except ValueError:
            logger.warning(f"Invalid IP address format: {value}")
            raise serializers.ValidationError("Invalid IP address format.")
        
        return value

    def create(self, validated_data):
        """
        Create a new SoilMoisture instance with logging.
        """
        logger.info(f"Creating new SoilMoisture record from IP: {validated_data.get('ip_address')}")
        instance = super().create(validated_data)
        logger.info(f"Successfully created SoilMoisture record with ID: {instance.id}")
        return instance

    def update(self, instance, validated_data):
        """
        Update a SoilMoisture instance with logging.
        """
        logger.info(f"Updating SoilMoisture record with ID: {instance.id}")
        instance = super().update(instance, validated_data)
        logger.info(f"Successfully updated SoilMoisture record with ID: {instance.id}")
        return instance

