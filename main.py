from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "yt-dlp proxy is running"}

@app.get("/stream")
def get_stream(videoId: str):
    if not videoId:
        raise HTTPException(status_code=400, detail="videoId is required")
    
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    url = f"https://www.youtube.com/watch?v={videoId}"
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            stream_url = info.get('url')
            if not stream_url:
                raise HTTPException(status_code=404, detail="Could not extract stream URL")
            
            # For now, we redirect the user directly to the googlevideo.com URL.
            # If YouTube blocks this due to IP binding, we can change this to 
            # proxy the stream using requests.get(stream_url, stream=True)
            return RedirectResponse(url=stream_url)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
