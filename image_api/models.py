from django.db import models

class ImageProcessingRequest(models.Model):
    request_id = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

class Product(models.Model):
    request = models.ForeignKey(ImageProcessingRequest, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    input_images = models.TextField()  # Store comma-separated URLs
    output_images = models.TextField(null=True, blank=True)
