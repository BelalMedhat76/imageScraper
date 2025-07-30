# import os
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin, urlparse

# # Fake browser headers
# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
# }

# # Create downloads folder if not exists
# DOWNLOAD_FOLDER = "downloads"
# os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# def get_images_from_url(url):
#     try:
#         # Fetch page
#         response = requests.get(url, headers=HEADERS, timeout=10)
#         response.raise_for_status()

#         soup = BeautifulSoup(response.text, 'html.parser')
#         images = []

#         for img_tag in soup.find_all('img'):
#             img_url = img_tag.get('src')
#             if img_url:
#                 full_url = urljoin(url, img_url)
#                 images.append(full_url)

#                 # Download image locally
#                 download_image(full_url)

#         return images
#     except Exception as e:
#         return {"error": str(e)}

# def download_image(img_url):
#     try:
#         # Get filename from URL
#         filename = os.path.basename(urlparse(img_url).path)
#         if not filename:  # if empty, make a default name
#             filename = "image.jpg"

#         file_path = os.path.join(DOWNLOAD_FOLDER, filename)

#         # Download and save
#         img_data = requests.get(img_url, headers=HEADERS, timeout=10).content
#         with open(file_path, "wb") as f:
#             f.write(img_data)
#         print(f"Downloaded: {file_path}")
#     except Exception as e:
#         print(f"Failed to download {img_url}: {e}")



import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Fake browser headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Create downloads folder if not exists
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def extract_best_image_url(img_tag, base_url):
    """Try to get the highest resolution image URL from the img tag."""
    # Try srcset (usually has multiple sizes)
    srcset = img_tag.get("srcset")
    if srcset:
        # Take the last (largest) image from srcset
        last_src = srcset.split(",")[-1].strip().split(" ")[0]
        return urljoin(base_url, last_src)

    # Try data-src / data-large for lazy-loaded images
    data_src = img_tag.get("data-src") or img_tag.get("data-large") or img_tag.get("data-original")
    if data_src:
        return urljoin(base_url, data_src)

    # Fallback: normal src
    src = img_tag.get("src")
    if src:
        return urljoin(base_url, src)

    return None

def download_image(img_url):
    """Download image in full resolution to downloads folder."""
    try:
        filename = os.path.basename(urlparse(img_url).path)
        if not filename:  # If filename is empty
            filename = "image.jpg"

        file_path = os.path.join(DOWNLOAD_FOLDER, filename)

        # Fetch image data
        r = requests.get(img_url, headers=HEADERS, timeout=15)
        r.raise_for_status()

        with open(file_path, "wb") as f:
            f.write(r.content)

        print(f"✅ Saved: {file_path}")
    except Exception as e:
        print(f"❌ Failed to download {img_url} — {e}")

def get_images_from_url(url):
    """Scrape and download all full-resolution images from the given URL."""
    try:
        # Fetch HTML content
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        images = []

        for img_tag in soup.find_all("img"):
            best_url = extract_best_image_url(img_tag, url)
            if best_url and best_url not in images:
                images.append(best_url)
                download_image(best_url)

        return images
    except Exception as e:
        return {"error": str(e)}
