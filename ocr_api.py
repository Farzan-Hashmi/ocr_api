from fastapi import FastAPI, Query
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
import os

app = FastAPI()


@app.get("/scrape")
async def scrape_text(youtube_url: str = Query(..., description="YouTube video URL")):
    ytt_api = YouTubeTranscriptApi(
        proxy_config=WebshareProxyConfig(
            proxy_username=os.getenv("PROXY_USERNAME"),
            proxy_password=os.getenv("PROXY_PASSWORD"),
        )
    )
    print("reached")
    video_id = youtube_url.split("v=")[-1].split("&")[0]
    print(video_id)
    transcript_dicts = ytt_api.fetch(video_id).to_raw_data()

    to_return = [
        {
            "id": video_id,
            "text": transcript["text"],
            "regular_url": f"https://www.youtube.com/watch?v={video_id}",
            "url_with_timestamp": f"https://www.youtube.com/watch?v={video_id}&t={transcript['start']}s",
            "thumbnail_url": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
        }
        for transcript in transcript_dicts
    ]

    return {"transcripts": to_return}
