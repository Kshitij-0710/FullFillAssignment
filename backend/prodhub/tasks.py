from celery import shared_task
from .models import Product, UploadJob
import csv
import io

@shared_task(bind=True)
def process_csv_upload(self, file_path, job_id):
    """
    Processes the CSV file asynchronously without loading large data into Django.
    """
    job = UploadJob.objects.get(job_id=job_id)
    job.status = "PROCESSING"
    job.save()

    try:
        products_map = {}

        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                sku = row.get('sku')
                if not sku:
                    continue

                normalized_sku = sku.strip().upper()

                products_map[normalized_sku] = Product(
                    sku=normalized_sku,
                    name=row.get('name', ''),
                    description=row.get('description', ''),
                    active=True
                )

        final_products_list = list(products_map.values())

        Product.objects.bulk_create(
            final_products_list,
            batch_size=5000,
            update_conflicts=True,
            unique_fields=['sku'],
            update_fields=['name', 'description', 'active']
        )

        job.status = "COMPLETED"
        job.progress_message = f"Successfully imported {len(final_products_list)} products."
        job.save()

    except Exception as e:
        job.status = "FAILED"
        job.error_message = str(e)
        job.save()

@shared_task
def bulk_delete_products():
    """
    Deletes all products asynchronously to avoid request timeouts.
    """
    try:
        Product.objects.all().delete()
        return "Successfully deleted all products."
    except Exception as e:
        return f"Error during bulk delete: {str(e)}"