from django.urls import path
from .views import WebhookView, UploadCSV, CheckStatus

urlpatterns = [
    path('webhook/', WebhookView.as_view(), name='webhook'),  # Endpoint for webhook
    path('upload/', UploadCSV.as_view(), name='process_images'),  # Endpoint to upload images
    path('status/<str:request_id>/', CheckStatus.as_view(), name='check_status'),  # Endpoint to check processing status
]
