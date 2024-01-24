import os
from io import BytesIO
from PIL import Image
import requests
import base64
import re

image_url = "blob:http://localhost:3000/68a45c69-6b0e-4005-ac02-8f55e97eccd5";
response = requests.get(image_url);
# file_path = r"model_files\best_full_weights.h5"
# response = requests.get(image_url)

image_data_match = re.search(r'blob:(.+)', image_url)
image_data_base64 = image_data_match.group(1)
# Decode the base64-encoded image data
image_data = base64.b64decode(image_data_base64)
print(image_data)

try:
    print("Image Data:", image_data[:50])
    image = Image.open(BytesIO(image_data));
    print("Image opened successfully")
except Exception as e:
    print(f'Error opening image: {str(e)}')


# print(os.path.exists(file_path))