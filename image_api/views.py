import csv
import uuid
from django.http import JsonResponse
from django.views import View
from .tasks import process_images
from .models import ImageProcessingRequest, Product
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class UploadCSV(View):
    def post(self, request):
        file = request.FILES.get('file')
        if not file.name.endswith('.csv'):
            return JsonResponse({'error': 'File must be a CSV.'}, status=400)

        request_id = str(uuid.uuid4())
        process_request = ImageProcessingRequest.objects.create(request_id=request_id)

        # Reading CSV and saving entries to the database
        reader = csv.reader(file.read().decode('utf-8').splitlines())
        next(reader)
        for row in reader:
            print(f'row --------------> {row}')
            Product.objects.create(
                request=process_request,
                product_name=row[1],
                input_images=row[2]
            )

        # Starting asynchronous processing (using Celery)
        process_images.delay(request_id)

        return JsonResponse({'request_id': request_id}, status=201)


class CheckStatus(View):
    def get(self, request, request_id):
        try:
            process_request = ImageProcessingRequest.objects.get(request_id=request_id)
            return JsonResponse({'status': 'processed' if process_request.is_processed else 'processing'})
        except ImageProcessingRequest.DoesNotExist:
            return JsonResponse({'error': 'Request ID not found'}, status=404)
        

@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(View):
    def post(self, request):
        print("Webhook received:", request.body)
        return JsonResponse({'status': 'success'}, status=200)