# Soundwave YT-DLP Proxy Backend

This is a tiny Python application designed to run on a free host like [Render.com](https://render.com) or [Koyeb](https://koyeb.com). It provides a `/stream` endpoint that uses `yt-dlp` to extract the direct audio URL for a given YouTube video and redirect the player to it.

## How to deploy on Render.com (Free)

1. Create a new GitHub repository for this folder and push the code:
   ```bash
   cd ytdlp-proxy
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ytdlp-proxy.git
   git push -u origin main
   ```
2. Go to [Render.com](https://render.com) and sign in.
3. Click **New +** and select **Web Service**.
4. Connect your GitHub account and select the `ytdlp-proxy` repository.
5. Setup the following settings:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Click **Create Web Service**. Wait 2-3 minutes for the build to finish.
7. Once deployed, Render will give you a URL like `https://ytdlp-proxy.onrender.com`.

**Important**: Once you have this URL, let me know what it is! I will update your frontend and `api.php` to use this new URL for background audio playback!
