# Homepage with Google Drive Assets

This project provides a simple homepage (`homepage.html`) that features:
- A slideshow of images pulled from a specified Google Drive folder.
- A background audio player playing random tracks from a separate Google Drive folder.

The assets are downloaded and stored in the repository using a GitHub Actions workflow, avoiding direct links to Google Drive to prevent blocking.

## Setup

1.  **Configure `config.json`:**
    Update the `config.json` file in the root directory with the shareable links to your Google Drive folders. Make sure the folders are publicly accessible (shared with "Anyone with the link").

    ```json
    {
        "audio_folder_url": "YOUR_AUDIO_FOLDER_DRIVE_URL_HERE",
        "images_folder_url": "YOUR_IMAGES_FOLDER_DRIVE_URL_HERE"
    }
    ```

2.  **Enable GitHub Pages:**
    - Go to your repository **Settings**.
    - Click on **Pages** in the left sidebar.
    - Under **Build and deployment**, select **Source** as "Deploy from a branch".
    - Select the branch (usually `main`) and folder `/ (root)`.
    - Click **Save**.
    - Your site will be published at `https://<username>.github.io/<repository-name>/`.

3.  **Install Dependencies (Local):**
    If you want to run the download script locally, you need Python and the required libraries.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the Automation Manually (GitHub Actions)

To update the assets without waiting for the scheduled daily run:

1.  Go to the **Actions** tab in your GitHub repository.
2.  Select the **Update Assets** workflow from the left sidebar.
3.  Click the **Run workflow** dropdown button on the right.
4.  Select the branch (usually `main`) and click the green **Run workflow** button.

This will trigger the workflow to:
- Download the latest files from the configured Google Drive folders.
- Update `assets/media_list.json` with the new file list.
- Commit and push any changes to the repository.

### Running Locally (Testing)

You can also run the download script on your local machine to test configuration or download assets immediately.

1.  Ensure you have installed the dependencies (see Setup above).
2.  Run the script:
    ```bash
    python scripts/download_assets.py
    ```

The script will download files into `assets/audio` and `assets/images` and update `assets/media_list.json`. Open `homepage.html` in your browser to see the changes.

## Embedding in Squarespace or WordPress

To display this homepage on your Squarespace or WordPress site, you can use the provided `embed_loader.html` snippet.

1.  Ensure GitHub Pages is enabled (see Setup).
2.  Open `embed_loader.html`.
3.  Replace `YOUR_GITHUB_PAGES_URL` with the full URL to your `homepage.html` (e.g., `https://username.github.io/repo/homepage.html`).
4.  Copy the code inside the file.
5.  In Squarespace or WordPress, add a **Code Block** or **Custom HTML** widget.
6.  Paste the code snippet.

## Project Structure

- `homepage.html`: The main HTML file for the site.
- `embed_loader.html`: HTML snippet for embedding the homepage via iframe.
- `config.json`: Configuration file for Google Drive folder URLs.
- `scripts/download_assets.py`: Python script to download assets using `gdown`.
- `.github/workflows/update_assets.yml`: GitHub Actions workflow for automated updates.
- `assets/`: Directory where downloaded media files are stored.
