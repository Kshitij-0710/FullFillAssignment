Product Importer API

A high-performance Django backend designed to import and manage 500,000+ product records asynchronously.

This system provides a robust REST API for product management, CSV imports, webhook testing, and large-scale operations without timeouts.

Tech Stack
Area	Technology	Reason
Backend	Django & DRF	Rapid, clean, powerful ModelViewSet APIs
Async Tasks	Celery	To run 500k+ CSV imports without timeouts
Message Broker	Redis	Celery’s job queue
Database	PostgreSQL	Stable concurrent writes (avoids SQLite lock issues)
Dev Infra	Docker	Easiest way to run Redis & Postgres locally
Features
Story 1 & 1A — Async CSV Upload + Progress Tracking

POST /api/products/upload/ accepts .csv, creates an UploadJob, and immediately queues a Celery task.

Celery task:

Deduplicates 500k+ rows in-memory using a Python dict.

Performs a single, fast bulk_create(update_conflicts=True) UPSERT.

Status polling:

GET /api/job/<uuid:job_id>/status/

Returns: PENDING, PROCESSING, COMPLETED, FAILED

Errors stored in UploadJob.error_message.

Story 2 — Full Product Management

/api/products/ — Full CRUD using DRF’s ModelViewSet

Filters:

?sku=ABC123
?active=true
?search=laptop


Pagination (default: 25 per page)

Story 3 — Bulk Delete

POST /api/products/bulk_delete/

Runs an async Celery task

API returns 202 Accepted instantly

Story 4 — Webhook Manager

/api/webhooks/ — Full CRUD

POST /api/webhooks/<id>/test/

Sends a real test payload to the webhook URL

Returns success or timeout/connection error

Local Setup & Installation
1. Prerequisites

Python 3.10+

Docker Desktop (must be running)

2. Clone Repository
git clone <your-repo-url>
cd <your-project-folder>

3. Backend Setup
Create & Activate Virtual Environment
python -m venv venv
source venv/bin/activate   # macOS / Linux
# OR
venv\Scripts\activate      # Windows

Install Dependencies
pip install -r requirements.txt

4. Start Required Docker Services
Terminal 1 — Start Redis
docker run -d --name prodhub-redis -p 6379:6379 redis

(Postgres is assumed to be running on port 5433)

Update product_importer/settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'prodhub_db',
        'USER': 'prodhub_user',
        'PASSWORD': 'mysecretpassword',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}

5. Run Django Server
cd <your-django-project-folder>   # e.g., product_importer

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

That's it!

You now have:

Async CSV import (500k+ records)

Product CRUD

Bulk delete via Celery

Webhook management + test endpoint

Full Docker-backed Redis & Postgres setup