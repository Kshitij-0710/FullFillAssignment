# Product Importer API

This is a high-performance Django backend designed to import and manage a large product catalog (500,000+ records) asynchronously.

It provides a full-featured REST API for product and webhook management, built to handle large-scale data operations without request timeouts.

---

## Tech Stack

| Area | Technology | Reason |
|------|------------|--------|
| Backend | Django & Django Rest Framework | Rapid, simple & powerful ModelViewSet APIs |
| Async Tasks | Celery | Handles 500k+ CSV import + bulk delete without timeouts |
| Message Broker | Redis | Job queue for Celery |
| Database | PostgreSQL | Handles concurrency; avoids SQLite lock issues |
| Dev Infra | Docker | Easiest way to run Redis & Postgres locally |

---

## Features

### Story 1 & 1A: Async CSV Upload & Progress

- POST `/api/products/upload/` accepts a CSV, creates an `UploadJob`, and queues a Celery task.
- Celery deduplicates 500k+ rows in-memory using a Python dict.
- Uses `bulk_create(update_conflicts=True)` for a single high-speed UPSERT.
- GET `/api/job/<uuid:job_id>/status/` returns: `PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`.
- Errors saved to the `UploadJob.error_message` field.

### Story 2: Full Product Management

- `/api/products/` supports full CRUD (ModelViewSet).
- Filtering: `?sku=ABC123`, `?active=true`
- Search: `?search=laptop`
- Pagination: default 25 per page.

### Story 3: Bulk Delete

- POST `/api/products/bulk_delete/` queues a Celery task.
- Returns `202 Accepted` immediately.

### Story 4: Webhook Manager

- `/api/webhooks/` full CRUD.
- POST `/api/webhooks/<id>/test/` sends a live test payload with `requests`.

---

## Local Setup & Installation

### 1. Prerequisites

- Python 3.10+
- Docker Desktop (running)

---

### 2. Clone Repository

```bash
git clone <your-repo-url>
cd <your-project-folder>
```


```

---

### 3. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Start Redis (Docker)

```bash
docker run -d --name prodhub-redis -p 6379:6379 redis
```

---

### 6. Start PostgreSQL (Docker)

```bash
docker run -d \
  --name prodhub-postgres \
  -e POSTGRES_DB=prodhub_db \
  -e POSTGRES_USER=prodhub_user \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5433:5432 \
  postgres:15
```

PostgreSQL is already configured in `product_importer/settings.py`:

```python
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
```

---

### 7. Run Database Migrations

```bash
cd backend
python manage.py migrate
```

---

### 8. Start Celery Worker

Open a new terminal and run:

```bash
cd backend
source ../venv/bin/activate  # Activate virtual environment
celery -A product_importer worker --loglevel=info
```

---

### 9. Start Django Development Server

In another terminal:

```bash
cd backend
source ../venv/bin/activate  # Activate virtual environment
python manage.py runserver
```

---

## API Endpoints

### Products

- `GET /api/products/` - List all products (with pagination, filtering, search)
- `POST /api/products/` - Create a new product
- `GET /api/products/{id}/` - Retrieve a specific product
- `PUT /api/products/{id}/` - Update a product
- `DELETE /api/products/{id}/` - Delete a product
- `POST /api/products/upload/` - Upload CSV file for bulk import
- `POST /api/products/bulk_delete/` - Bulk delete products
- `GET /api/job/{job_id}/status/` - Check upload job status

### Webhooks

- `GET /api/webhooks/` - List all webhooks
- `POST /api/webhooks/` - Create a new webhook
- `GET /api/webhooks/{id}/` - Retrieve a specific webhook
- `PUT /api/webhooks/{id}/` - Update a webhook
- `DELETE /api/webhooks/{id}/` - Delete a webhook
- `POST /api/webhooks/{id}/test/` - Test a webhook

---

## Testing the API

You can test the API using:
- **Postman**: Import the endpoints and test
- **curl**: Command-line HTTP requests
- **Django REST Framework UI**: Navigate to `http://localhost:8000/api/` in your browser

### Example: Upload CSV

```bash
curl -X POST http://localhost:8000/api/products/upload/ \
  -F "file=@products.csv"
```

### Example: Check Job Status

```bash
curl http://localhost:8000/api/job/{job_id}/status/
```

---

## Troubleshooting

### Redis Connection Error
Ensure Redis container is running:
```bash
docker ps | grep prodhub-redis
```

If not running, start it:
```bash
docker start prodhub-redis
```

### PostgreSQL Connection Error
Ensure PostgreSQL container is running:
```bash
docker ps | grep prodhub-postgres
```

If not running, start it:
```bash
docker start prodhub-postgres
```

### Celery Worker Not Processing Tasks
Make sure the Celery worker is running in a separate terminal with the correct app name and settings.

---

## Project Structure

```
FilloAssignment/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── db.sqlite3
│   ├── prodhub/          # Main app for product management
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── tasks.py      # Celery tasks
│   │   └── migrations/
│   ├── webhook/          # Webhook management app
│   │   ├── models.py
│   │   ├── views.py
│   │   └── serializers.py
│   └── product_importer/ # Django project settings
│       ├── settings.py
│       ├── urls.py
│       ├── celery.py
│       └── routing.py
├── frontend/             # React frontend (optional)
└── products.csv          # Sample CSV file
```

---

## License

This project is licensed under the MIT License.


---
