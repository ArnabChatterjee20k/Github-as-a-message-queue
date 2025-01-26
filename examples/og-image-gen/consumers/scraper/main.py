from playwright.sync_api import sync_playwright
import cloudinary
import cloudinary.uploader
import redis
import os
import json

def get_secret_val(key:str):
    all_secrets = json.loads(os.environ.get('ALL_SECRETS', '{}'))
    # Get the entire variables context
    # all_vars = json.loads(os.environ.get('ALL_VARS', '{}'))
    
    return all_secrets.get(key.upper())

# Playwright function to scrape and take a screenshot
def scrape(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        screenshot_path = f"screenshot_{url.split('//')[-1].replace('.', '_')}.png"
        page.screenshot(path=screenshot_path, full_page=True)
        browser.close()
        return screenshot_path


# Cloudinary function to upload image and return public URL
def upload(image_path):
    cloudinary_secret = get_secret_val("cloudinary_secret")
    # Configure Cloudinary credentials
    cloudinary.config( 
    cloud_name = "dgnavrggs", 
    api_key = "317788959676849", 
    api_secret = cloudinary_secret,
    secure=True
    )

    upload_result = cloudinary.uploader.upload(image_path)
    return upload_result["secure_url"]


# Redis function to save the image URL
def save_to_redis(uid, image_url):
    redis_password = get_secret_val("redis_password")
    r = redis.Redis(
    host='redis-15902.c256.us-east-1-2.ec2.redns.redis-cloud.com',
    port=15902,
    decode_responses=True,
    username="default",
    password=redis_password,
)
    r.set(uid, image_url)


# Main function to call all components
def main():
    uid = os.environ.get("ISSUE_TITLE").strip()
    url = os.environ.get("ISSUE_BODY").strip()
    try:
        # Step 1: Scrape and take a screenshot
        screenshot_path = scrape(url)

        # Step 2: Upload the screenshot to Cloudinary
        image_url = upload(screenshot_path)

        # Step 3: Save the public URL to Redis
        save_to_redis(uid, image_url)
        print(f"Successfully processed {uid}: {image_url}")
        print(image_url)
    except Exception as e:
        print(f"Error processing {uid}: {str(e)}")

main()
