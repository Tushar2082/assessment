from celery import shared_task
from .image_storage import save_image_to_storage
from .models import Product, ImageProcessingRequest
from PIL import Image
import requests
from io import BytesIO

@shared_task
def process_images(request_id):
    process_request = ImageProcessingRequest.objects.get(request_id=request_id)
    products = Product.objects.filter(request=process_request)

    for product in products:
        input_urls = product.input_images.split(',')
        output_urls = []
        print(f'input_urls --------------> {input_urls}')
        for url in input_urls:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))

            if img.mode == 'RGBA':
                img = img.convert('RGB')

            # Compressing image
            output_io = BytesIO()
            img.save(output_io, 'JPEG', quality=50)
            output_url = save_image_to_storage(output_io)
            output_urls.append(output_url)

        # Saving output image URLs
        product.output_images = ','.join(output_urls)
        product.save()

    # Marking the request as processed
    process_request.is_processed = True
    process_request.save()


    # Webhook triggering
    webhook_url = 'http://127.0.0.1:8000/image_api/webhook/'
    payload = {
        'request_id': request_id,
        'status': 'completed'
    }
    try:
        response = requests.post(webhook_url, json=payload)
        print(f"Webhook triggered: {response.status_code}")
    except Exception as e:
        print(f"Failed to trigger webhook: {e}")
