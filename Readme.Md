# Product Importer - Full Stack Application

A high-performance full-stack application for managing large product catalogs (500,000+ records) with asynchronous processing capabilities.

---

## 🌐 Live Project

| Service | URL |
|---------|-----|
| **Frontend** | [https://full-fill-assignment.vercel.app](https://full-fill-assignment.vercel.app) |
| **Backend API** | [https://fullfill.kshitijmoghe.tech/api/](https://fullfill.kshitijmoghe.tech/api/) |
| **API Docs (ReDoc)** | [https://fullfill.kshitijmoghe.tech/redoc/](https://fullfill.kshitijmoghe.tech/redoc/) |

---

## 📁 Project Structure

This project consists of two main components:

### 🔧 Backend - Django REST API
**Location**: `/backend`  
**Documentation**: [Readme.Backend.md](./Readme.Backend.md)

A Django-based REST API with Celery for asynchronous task processing, handling large-scale CSV imports and product management.

**Key Technologies**:
- Django & Django REST Framework
- Celery (async task queue)
- Redis (message broker)
- PostgreSQL (database)
- Docker (infrastructure)

**Features**:
- Async CSV upload (500k+ records)
- Full CRUD product management
- Bulk delete operations
- Webhook management
- ReDoc API documentation

---

### 🎨 Frontend - React Application
**Location**: `/frontend`  
**Documentation**: [Readme.Frontend.md](./Readme.Frontend.md)

A modern React frontend built with Vite, providing an intuitive UI for product and webhook management.

**Key Technologies**:
- React 19.2.0
- Vite 7.2.2
- Axios
- Modern CSS

**Features**:
- Drag-and-drop CSV upload
- Real-time job status tracking
- Product search & filtering
- Webhook testing interface
- Responsive design

---

## 🛠️ Tech Stack Summary

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | React + Vite | Fast, modern UI |
| Backend | Django + DRF | RESTful API |
| Task Queue | Celery | Async processing |
| Message Broker | Redis | Task distribution |
| Database | PostgreSQL | Data persistence |
| Infrastructure | Docker | Service orchestration |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker Desktop

### Setup Instructions

For detailed setup and configuration instructions, please refer to:

- **Backend Setup**: [Readme.Backend.md](./Readme.Backend.md)
- **Frontend Setup**: [Readme.Frontend.md](./Readme.Frontend.md)

---

## 📚 Documentation

For detailed setup, configuration, and usage instructions:

- **Backend Documentation**: [Readme.Backend.md](./Readme.Backend.md)
  - API endpoints
  - Database configuration
  - Celery task management
  - Troubleshooting

- **Frontend Documentation**: [Readme.Frontend.md](./Readme.Frontend.md)
  - Component overview
  - Build and deployment
  - Environment configuration
  - Styling guide

---

## 🔗 Key URLs

### 🌐 Live Deployment

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | https://full-fill-assignment.vercel.app | Live React application |
| **Backend API** | https://fullfill.kshitijmoghe.tech/api/ | Live REST API endpoints |
| **API Docs (ReDoc)** | https://fullfill.kshitijmoghe.tech/redoc/ | Interactive API documentation |

### 💻 Local Development

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | React application |
| Backend API | http://localhost:8000/api/ | REST API endpoints |
| API Docs (ReDoc) | http://localhost:8000/redoc/ | Interactive API documentation |
| Django Admin | http://localhost:8000/admin/ | Django admin panel |

---

## 📦 Features Overview

### Story 1 & 1A: CSV Upload with Progress Tracking
- Upload large CSV files (500k+ records)
- Real-time job status updates
- Asynchronous processing with Celery

**⚡ Upload Performance Note:**  
Initial file upload may take 14–25 seconds for large files (80–90MB). This delay is due to network upload time from browser to server, not backend processing. Once the file reaches the server, the backend responds instantly and processing happens asynchronously in the background.

*Future Enhancement:* Direct uploads to AWS S3 using presigned URLs can eliminate this delay entirely by uploading directly from browser to S3's high-speed pipeline, with the API only receiving the S3 file reference.

### Story 2: Product Management
- Full CRUD operations
- Search and filtering
- Pagination support

### Story 3: Bulk Operations
- Bulk delete all products
- Background task processing

### Story 4: Webhook Management
- Create and manage webhooks
- Test webhook endpoints
- Event-based notifications

---


## 📞 Support

For issues or questions:
- Check the troubleshooting sections in backend/frontend docs
- Review API documentation at `/redoc/`
- Inspect browser console for frontend errors
- Check Django logs for backend errors
