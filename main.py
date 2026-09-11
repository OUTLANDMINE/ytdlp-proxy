from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import requests

import os

app = FastAPI()

# Add your YouTube cookies here or set them in Render Environment Variables
YOUTUBE_COOKIES = os.environ.get("YOUTUBE_COOKIES", """__Secure-3PSID=g.a000Cgk0ULT6j33vK1e8U4SdmVqyNU9i58GZKdIinlkqWDbWbTjjaN4_xUPWw5WmBg1ZSvstlgACgYKAW0SARQSFQHGX2MiJZ__39Zcv8RA9woRbiL9KBoVAUF8yKqbQqEBAxBBgc5GD-uSDWZz0076;GPS=1;__Secure-1PSIDTS=sidts-CjUBXMw41a2Bbqxub3RIlnx4q1PsV7K_UQtXSLVdZue7aBwCMfNr6cBH4OONOUYvrmnHvQUQjxAA;SAPISID=ESWN0wzfrGp6iHx5/Axe5I_VZ2q62J4wWM;__Secure-1PSIDCC=AKEyXzW3S4MQg34HxzLNX5dTILUkBZRANh3VUeT9ASHwqq7Vf8nCMSOs_n0dwD-HYTx5rjOtXw;SSID=AQFT89Q6tLURuuMqp;__Secure-1PAPISID=ESWN0wzfrGp6iHx5/Axe5I_VZ2q62J4wWM;__Secure-1PSID=g.a000Cgk0ULT6j33vK1e8U4SdmVqyNU9i58GZKdIinlkqWDbWbTjj5RfiauoBi7EonHRf4k3cNQACgYKAcgSARQSFQHGX2Mi47b3V8bAZvEzBFADySbcxhoVAUF8yKp7YeDWAxMhlplVJ_UtIIaa0076;__Secure-3PAPISID=ESWN0wzfrGp6iHx5/Axe5I_VZ2q62J4wWM;__Secure-3PSIDCC=AKEyXzV7D9OohjU7Znj7N-AqJI2fRZepKUhcO0Wg-MhhyMr9M9J4kf34VNo4dE9g-H78os-S;__Secure-3PSIDTS=sidts-CjUBXMw41a2Bbqxub3RIlnx4q1PsV7K_UQtXSLVdZue7aBwCMfNr6cBH4OONOUYvrmnHvQUQjxAA;LOGIN_INFO=AFmmF2swRgIhAMd04JDM5uxQm7L8ljUJkAudZ-aGErB9CqU1SSq5SiU7AiEAi9PU7zBbCHVlAovk72G92Ssug3ZDzitbYYCBRrwZcTw:QUQ3MjNmeGdkOFluWXduTUNVUl9aVDVjRkdiV1ZmOFhUN0JqV21sdEVVcDVpZmNmeFBBRzhmX1lIX3BqemlOd1FoRGZ1OG15MXNQSGIzXzVRdi1LTGx1eFNkUTNzVXVaVmlicnJHMzRPaEpQaWJmUFVyNEVTbjdKVFV5M3ZQcDZucVFRb0t5bW0yQXBRSS1oblkzSDU0YmNSWjk3TnVNRTZn;PREF=f6=40000080&tz=Asia.Calcutta""")

if YOUTUBE_COOKIES:
    with open("cookies.txt", "w") as f:
        f.write("# Netscape HTTP Cookie File\n")
        for cookie in YOUTUBE_COOKIES.split(';'):
            cookie = cookie.strip()
            if not cookie: continue
            parts = cookie.split('=', 1)
            if len(parts) == 2:
                f.write(f".youtube.com\tTRUE\t/\tTRUE\t1893456000\t{parts[0]}\t{parts[1]}\n")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "yt-dlp proxy is running with cookies!"}

@app.get("/stream")
def get_stream(videoId: str):
    if not videoId:
        raise HTTPException(status_code=400, detail="videoId is required")
    
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    if os.path.exists("cookies.txt"):
        ydl_opts['cookiefile'] = "cookies.txt"
    
    url = f"https://www.youtube.com/watch?v={videoId}"
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            stream_url = info.get('url')
            if not stream_url:
                raise HTTPException(status_code=404, detail="Could not extract stream URL")
            
            return RedirectResponse(url=stream_url)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
