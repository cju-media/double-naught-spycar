import json
import os
import shutil
import gdown

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def download_folder(url, output_folder):
    if not url or "YOUR_" in url:
        print(f"Skipping download for {output_folder}: Invalid or placeholder URL.")
        return

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    try:
        gdown.download_folder(url, output=output_folder, quiet=False, use_cookies=False)
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def generate_media_list(audio_dir, images_dir, output_file):
    media_list = {
        "audio": [],
        "images": []
    }

    # Walk through audio directory
    if os.path.exists(audio_dir):
        for root, _, files in os.walk(audio_dir):
            for file in files:
                if file.lower().endswith(('.mp3', '.wav', '.ogg')):
                    # Create relative path from repo root
                    rel_path = os.path.relpath(os.path.join(root, file), ".")
                    media_list["audio"].append(rel_path.replace("\\", "/"))

    # Walk through images directory
    if os.path.exists(images_dir):
        for root, _, files in os.walk(images_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                    rel_path = os.path.relpath(os.path.join(root, file), ".")
                    media_list["images"].append(rel_path.replace("\\", "/"))

    with open(output_file, 'w') as f:
        json.dump(media_list, f, indent=4)
    print(f"Media list generated at {output_file}")

def main():
    config = load_config()

    audio_url = config.get('audio_folder_url')
    images_url = config.get('images_folder_url')

    audio_dir = 'assets/audio'
    images_dir = 'assets/images'

    print(f"Downloading audio to {audio_dir}...")
    download_folder(audio_url, audio_dir)

    print(f"Downloading images to {images_dir}...")
    download_folder(images_url, images_dir)

    generate_media_list(audio_dir, images_dir, 'assets/media_list.json')

if __name__ == "__main__":
    main()
