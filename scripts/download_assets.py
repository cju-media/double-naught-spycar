import json
import os
import shutil
import subprocess
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

def convert_to_mp3(file_path):
    output_path = os.path.splitext(file_path)[0] + '.mp3'
    try:
        # -y: overwrite output files, -vn: disable video, -ar: audio rate, -ac: audio channels, -b:a: audio bitrate
        cmd = ['ffmpeg', '-y', '-i', file_path, '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k', output_path]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(file_path)
        print(f"Converted {file_path} to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {file_path}: {e}")
    except FileNotFoundError:
        print("Error: ffmpeg is not installed or not in PATH. Please install ffmpeg.")

def process_audio_files(audio_dir):
    if not os.path.exists(audio_dir):
        return

    for root, _, files in os.walk(audio_dir):
        for file in files:
            if file.lower().endswith(('.wav', '.aif', '.aiff')):
                file_path = os.path.join(root, file)
                convert_to_mp3(file_path)

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

    print(f"Processing audio files in {audio_dir}...")
    process_audio_files(audio_dir)

    print(f"Downloading images to {images_dir}...")
    download_folder(images_url, images_dir)

    generate_media_list(audio_dir, images_dir, 'assets/media_list.json')

if __name__ == "__main__":
    main()
