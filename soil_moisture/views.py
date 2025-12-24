import logging
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import SoilMoisture
from .serializers import SoilMoistureSerializer
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger('soil_moisture')


def create_response(success=True, data=None, message=None, errors=None, status_code=status.HTTP_200_OK):
    """
    Create a structured response format for all API endpoints.
    """
    response_data = {
        'success': success,
    }
    
    if data is not None:
        response_data['data'] = data
    
    if message:
        response_data['message'] = message
    
    if errors:
        response_data['errors'] = errors
    
    return Response(response_data, status=status_code)


@api_view(['GET'])
def list_soil_moisture(request):
    """
    GET endpoint to retrieve all SoilMoisture records.
    Supports pagination via query parameters: page, page_size
    """
    try:
        logger.info(f"GET request received from IP: {request.META.get('REMOTE_ADDR')}")
        
        # Get pagination parameters
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 100)
        
        try:
            page = int(page)
            page_size = int(page_size)
        except ValueError:
            logger.warning(f"Invalid pagination parameters: page={page}, page_size={page_size}")
            return create_response(
                success=False,
                errors={'pagination': 'Page and page_size must be integers'},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate pagination parameters
        if page < 1:
            return create_response(
                success=False,
                errors={'page': 'Page must be greater than 0'},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        if page_size < 1 or page_size > 1000:
            return create_response(
                success=False,
                errors={'page_size': 'Page size must be between 1 and 1000'},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate offset
        offset = (page - 1) * page_size
        
        # Query database
        queryset = SoilMoisture.objects.all()
        total_count = queryset.count()
        records = queryset[offset:offset + page_size]
        
        serializer = SoilMoistureSerializer(records, many=True)
        
        logger.info(f"Retrieved {len(records)} records (page {page}, total: {total_count})")
        
        return create_response(
            success=True,
            data={
                'records': serializer.data,
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total_count': total_count,
                    'total_pages': (total_count + page_size - 1) // page_size if total_count > 0 else 0
                }
            },
            message='Records retrieved successfully'
        )
    
    except Exception as e:
        logger.error(f"Error retrieving SoilMoisture records: {str(e)}", exc_info=True)
        return create_response(
            success=False,
            errors={'detail': 'An error occurred while retrieving records'},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def create_soil_moisture(request):
    """
    POST endpoint to create a new SoilMoisture record.
    """
    try:
        logger.info(f"POST request received from IP: {request.META.get('REMOTE_ADDR')}")
        
        # Extract IP address from request if not provided
        data = request.data.copy()
        if 'ip_address' not in data:
            data['ip_address'] = request.META.get('REMOTE_ADDR', 'unknown')
        
        serializer = SoilMoistureSerializer(data=data)
        
        if serializer.is_valid():
            instance = serializer.save()
            logger.info(f"Successfully created SoilMoisture record with ID: {instance.id}")
            
            return create_response(
                success=True,
                data=serializer.data,
                message='Record created successfully',
                status_code=status.HTTP_201_CREATED
            )
        else:
            logger.warning(f"Validation errors: {serializer.errors}")
            return create_response(
                success=False,
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
    except IntegrityError as e:
        logger.error(f"Integrity error creating record: {str(e)}")
        return create_response(
            success=False,
            errors={'detail': 'Database integrity error occurred'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    except Exception as e:
        logger.error(f"Error creating SoilMoisture record: {str(e)}", exc_info=True)
        return create_response(
            success=False,
            errors={'detail': 'An error occurred while creating the record'},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
def update_soil_moisture(request, pk):
    """
    PUT endpoint to update an existing SoilMoisture record.
    """
    try:
        logger.info(f"PUT request received for ID: {pk} from IP: {request.META.get('REMOTE_ADDR')}")
        
        try:
            instance = SoilMoisture.objects.get(pk=pk)
        except SoilMoisture.DoesNotExist:
            logger.warning(f"SoilMoisture record with ID {pk} not found")
            return create_response(
                success=False,
                errors={'detail': 'Record not found'},
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        serializer = SoilMoistureSerializer(instance, data=request.data, partial=False)
        
        if serializer.is_valid():
            instance = serializer.save()
            logger.info(f"Successfully updated SoilMoisture record with ID: {instance.id}")
            
            return create_response(
                success=True,
                data=serializer.data,
                message='Record updated successfully'
            )
        else:
            logger.warning(f"Validation errors: {serializer.errors}")
            return create_response(
                success=False,
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        return create_response(
            success=False,
            errors={'detail': str(e)},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    except Exception as e:
        logger.error(f"Error updating SoilMoisture record: {str(e)}", exc_info=True)
        return create_response(
            success=False,
            errors={'detail': 'An error occurred while updating the record'},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
def delete_soil_moisture(request, pk):
    """
    DELETE endpoint to delete a SoilMoisture record.
    """
    try:
        logger.info(f"DELETE request received for ID: {pk} from IP: {request.META.get('REMOTE_ADDR')}")
        
        try:
            instance = SoilMoisture.objects.get(pk=pk)
        except SoilMoisture.DoesNotExist:
            logger.warning(f"SoilMoisture record with ID {pk} not found")
            return create_response(
                success=False,
                errors={'detail': 'Record not found'},
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        instance_id = instance.id
        instance.delete()
        logger.info(f"Successfully deleted SoilMoisture record with ID: {instance_id}")
        
        return create_response(
            success=True,
            message=f'Record {instance_id} deleted successfully',
            status_code=status.HTTP_200_OK
        )
    
    except Exception as e:
        logger.error(f"Error deleting SoilMoisture record: {str(e)}", exc_info=True)
        return create_response(
            success=False,
            errors={'detail': 'An error occurred while deleting the record'},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@csrf_exempt
@api_view(["POST"])
def receive_soil_moisture(request):
    print("Received JSON:", request.data)

    serializer = SoilMoistureSerializer(data={
        "data": request.data.get("data"),
        "metadata": request.data.get("metadata"),
        "ip_address": request.META.get("REMOTE_ADDR"),
    })

    if serializer.is_valid():
        serializer.save()
        return Response({"status": "ok"}, status=201)

    return Response(serializer.errors, status=400)
