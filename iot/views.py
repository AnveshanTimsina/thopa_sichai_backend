import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import SoilMoisture
from .serializers import SoilMoistureSerializer
from .services import determine_motor_state
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger('iot')


def create_response(success=True, data=None, message=None, errors=None, status_code=status.HTTP_200_OK):
    """
    Create a structured response format for all API endpoints.
    """
    response_data = {'success': success}
    if data is not None:
        response_data['data'] = data
    if message:
        response_data['message'] = message
    if errors:
        response_data['errors'] = errors
    return Response(response_data, status=status_code)


class IotPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000
    
    def get_paginated_response(self, data):
        return create_response(
            success=True,
            data={
                'records': data,
                'pagination': {
                    'page': self.page.number,
                    'page_size': self.page.paginator.per_page,
                    'total_count': self.page.paginator.count,
                    'total_pages': self.page.paginator.num_pages
                }
            },
            message='Records retrieved successfully'
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_iot(request):
    """
    GET endpoint to retrieve all SoilMoisture records.
    Supports pagination via query parameters: page, page_size
    """
    try:
        logger.info("GET request received from IP: %s", request.META.get('REMOTE_ADDR'))
        
        queryset = SoilMoisture.objects.all()
        paginator = IotPagination()
        
        try:
            paginated_queryset = paginator.paginate_queryset(queryset, request)
        except Exception as e:
            logger.warning("Pagination error: %s", str(e))
            return create_response(
                success=False,
                errors={'pagination': 'Invalid pagination parameters'},
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
        serializer = SoilMoistureSerializer(paginated_queryset, many=True)
        logger.info("Retrieved %d records for current page.", len(paginated_queryset))
        
        return paginator.get_paginated_response(serializer.data)
    
    except Exception as e:
        logger.exception("Error retrieving records")
        return create_response(
            success=False,
            errors={'detail': 'An error occurred while retrieving records'},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_iot(request):
    """
    POST endpoint to create a new SoilMoisture record.
    """
    try:
        remote_ip = request.META.get('REMOTE_ADDR', 'unknown')
        logger.info("POST request received from IP: %s", remote_ip)
        
        data = request.data.copy()
        if 'ip_address' not in data:
            data['ip_address'] = remote_ip
        
        serializer = SoilMoistureSerializer(data=data)
        
        if serializer.is_valid():
            instance = serializer.save()
            return create_response(
                success=True,
                data=serializer.data,
                message='Record created successfully',
                status_code=status.HTTP_201_CREATED
            )
            
        logger.warning("Validation errors: %s", serializer.errors)
        return create_response(
            success=False,
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    except IntegrityError:
        logger.error("Integrity error creating record", exc_info=True)
        return create_response(
            success=False,
            errors={'detail': 'Database integrity error occurred'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    except Exception:
        logger.exception("Error creating record")
        return create_response(
            success=False,
            errors={'detail': 'An error occurred while creating the record'},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_iot(request, pk):
    """
    PUT endpoint to update an existing SoilMoisture record.
    """
    try:
        logger.info("PUT request received for ID: %s from IP: %s", pk, request.META.get('REMOTE_ADDR'))
        
        try:
            instance = SoilMoisture.objects.get(pk=pk)
        except SoilMoisture.DoesNotExist:
            logger.warning("SoilMoisture record with ID %s not found", pk)
            return create_response(
                success=False,
                errors={'detail': 'Record not found'},
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        serializer = SoilMoistureSerializer(instance, data=request.data, partial=False)
        
        if serializer.is_valid():
            instance = serializer.save()
            return create_response(
                success=True,
                data=serializer.data,
                message='Record updated successfully'
            )
            
        logger.warning("Validation errors: %s", serializer.errors)
        return create_response(
            success=False,
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    except ValidationError as e:
        logger.error("Validation error: %s", str(e))
        return create_response(
            success=False,
            errors={'detail': str(e)},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    except Exception:
        logger.exception("Error updating record")
        return create_response(
            success=False,
            errors={'detail': 'An error occurred while updating the record'},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_iot(request, pk):
    """
    DELETE endpoint to delete a SoilMoisture record.
    """
    try:
        logger.info("DELETE request received for ID: %s from IP: %s", pk, request.META.get('REMOTE_ADDR'))
        
        try:
            instance = SoilMoisture.objects.get(pk=pk)
        except SoilMoisture.DoesNotExist:
            logger.warning("SoilMoisture record with ID %s not found", pk)
            return create_response(
                success=False,
                errors={'detail': 'Record not found'},
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        instance_id = instance.id
        instance.delete()
        logger.info("Successfully deleted SoilMoisture record with ID: %s", instance_id)
        
        return create_response(
            success=True,
            message=f'Record {instance_id} deleted successfully',
            status_code=status.HTTP_200_OK
        )
    
    except Exception:
        logger.exception("Error deleting record")
        return create_response(
            success=False,
            errors={'detail': 'An error occurred while deleting the record'},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def receive_iot(request):
    """
    Special POST endpoint for ESP32 payload ingestion.
    """
    logger.info("Received iot data payload.")

    serializer = SoilMoistureSerializer(data={
        "data": request.data.get("data"),
        "metadata": request.data.get("metadata"),
        "ip_address": request.META.get("REMOTE_ADDR"),
    })

    if serializer.is_valid():
        serializer.save()
        return Response({"status": "ok"}, status=status.HTTP_201_CREATED)

    logger.warning("Invalid ESP32 iot payload: %s", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def latest_iot(request):
    """
    GET endpoint to retrieve the latest SoilMoisture record and motor decision.
    """
    try:
        DEFAULT_THRESHOLD = 40.0
        threshold_param = request.query_params.get('threshold')

        if threshold_param is None:
            threshold = DEFAULT_THRESHOLD
        else:
            try:
                threshold = float(threshold_param)
            except ValueError:
                return create_response(
                    success=False,
                    errors={'threshold': 'Threshold must be a numeric value.'},
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        latest = SoilMoisture.objects.order_by('-created_at').first()

        if latest is None:
            return create_response(
                success=False,
                errors={'detail': 'No SoilMoisture records found.'},
                status_code=status.HTTP_404_NOT_FOUND
            )

        motor_decision = determine_motor_state(latest.data, threshold)

        return Response({
            'motor_state': motor_decision.get('motor_state'),
            'reading_value': motor_decision.get('reading_value'),
        }, status=status.HTTP_200_OK)

    except Exception:
        logger.exception("Error retrieving latest record")
        return create_response(
            success=False,
            errors={'detail': 'An error occurred while retrieving the latest record'},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
