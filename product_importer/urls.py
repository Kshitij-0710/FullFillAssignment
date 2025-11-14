from django.contrib import admin
from django.urls import path, include
from .routing import router
from .docs import schema_view
from prodhub import views as prodhub_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)), 
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path('api/job/<uuid:job_id>/status/', prodhub_views.JobStatusView.as_view(), name='job-status'),
]
