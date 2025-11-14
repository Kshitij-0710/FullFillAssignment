from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import bulk_delete_products, process_csv_upload
from .models import UploadJob

class ProductViewSet(viewsets.ModelViewSet):
    """
    This single ViewSet provides all CRUD operations for Products.
    It also handles filtering and searching.
    """
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sku', 'name', 'active'] 
    search_fields = ['sku', 'name', 'description'] 
    ordering_fields = ['name', 'sku'] 


class ProductUploadView(APIView):
    """
    Handles the file upload and starts the async task. (Story 1)
    """
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            file_content = file.read().decode('utf-8')
        except UnicodeDecodeError:
             return Response({"error": "File is not UTF-8 encoded."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 1. Create a job tracker
        job = UploadJob.objects.create(status="PENDING")
        
        # 2. Start the Celery task, passing it the content and job ID
        process_csv_upload.delay(file_content, job.job_id)
        
        # 3. Return the job ID to the client so it can poll for status
        return Response({"job_id": job.job_id}, status=status.HTTP_202_ACCEPTED)

class JobStatusView(APIView):
    """
    Reports the status of an upload job. (Story 1A)
    """
    def get(self, request, job_id, *args, **kwargs):
        try:
            job = UploadJob.objects.get(job_id=job_id)
            return Response({
                "job_id": job.job_id,
                "status": job.status,
                "progress": job.progress_message,
                "error": job.error_message,
            })
        except UploadJob.DoesNotExist:
            return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)
        


class ProductBulkDeleteView(APIView):
    """
    Triggers the async bulk delete task. (Story 3)
    """
    def post(self, request, *args, **kwargs):
        # Start the async delete task
        bulk_delete_products.delay()
        
        return Response(
            {"message": "Bulk delete task started. All products will be deleted in the background."},
            status=status.HTTP_202_ACCEPTED
        )
    

