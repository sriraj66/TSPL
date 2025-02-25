import os
import csv
import requests
import threading
from queue import Queue

# Configuration
CSV_FILE = "players.csv"  # Change this to your actual CSV file
IMAGE_FOLDER = "player_images"
BASE_URL = "https://tntenniscricket.in/media/"
THREAD_COUNT = 5

# Create folder if not exists
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Read CSV and prepare queue
def read_csv(file_path):
    queue = Queue()
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("player_image") and row.get("reg_id"):
                image_url = BASE_URL + row["player_image"].strip()
                filename = os.path.join(IMAGE_FOLDER, f"{row['reg_id'].strip()}.jpg")
                queue.put((image_url, filename))
    return queue

# Function to download an image
def download_image():
    while not image_queue.empty():
        image_url, filename = image_queue.get()
        try:
            response = requests.get(image_url, stream=True, timeout=10)
            if response.status_code == 200:
                with open(filename, 'wb') as img_file:
                    for chunk in response.iter_content(1024):
                        img_file.write(chunk)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download {image_url}")
        except Exception as e:
            print(f"Error downloading {image_url}: {e}")
        finally:
            image_queue.task_done()

# Load queue
image_queue = read_csv(CSV_FILE)

# Create and start threads
threads = []
for _ in range(THREAD_COUNT):
    thread = threading.Thread(target=download_image)
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()

print("All images downloaded.")
