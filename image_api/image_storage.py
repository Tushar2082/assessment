import os
import time
import uuid
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def save_image_to_storage(output_io):
    image_directory = 'C:\\Users\\tusha\\image_processing_project\\image_processor'

    if not os.path.exists(image_directory):
        os.makedirs(image_directory)

    image_name = f'processed_image_output_{uuid.uuid4()}.jpg'
    image_path = os.path.join(image_directory, image_name)

    default_storage.save(image_path, ContentFile(output_io.getvalue()))

    return f'http://localhost:8000/{image_path}'
