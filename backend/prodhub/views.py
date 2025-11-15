# prodhub/views.py
from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, UploadJob
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .tasks import bulk_delete_products, process_csv_upload
import os

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sku', 'name', 'active']
    search_fields = ['sku', 'name', 'description']
    ordering_fields = ['name', 'sku']

    @action(detail=False, methods=['post'])
    def upload(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        # Save to shared volume
        upload_dir = "/app/uploads"
        os.makedirs(upload_dir, exist_ok=True)

        temp_path = os.path.join(upload_dir, file.name)

        with open(temp_path, "wb+") as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        # Create job
        job = UploadJob.objects.create(status="PENDING")

        # Trigger Celery with PATH, not content
        process_csv_upload.delay(temp_path, job.job_id)

        return Response({"job_id": job.job_id}, status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=['post'])
    def bulk_delete(self, request, *args, **kwargs):
        bulk_delete_products.delay()
        return Response(
            {"message": "Bulk delete task started."},
            status=status.HTTP_202_ACCEPTED
        )


class JobStatusView(APIView):
    def get(self, request, job_id, *args, **kwargs):
        try:
            job = UploadJob.objects.get(job_id=job_id)
        except UploadJob.DoesNotExist:
            return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "job_id": job.job_id,
            "status": job.status,
            "progress": job.progress_message,
            "error": job.error_message,
        })
