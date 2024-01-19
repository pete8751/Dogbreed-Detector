import os
import requests
image_url = "blob:http://localhost:3000/a931421d-3d1c-449f-8ecd-b05f833ad707";
# file_path = r"model_files\best_full_weights.h5"
response = requests.get(image_url)
# print(os.path.exists(file_path))