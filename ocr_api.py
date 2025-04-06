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
    # {
    #     "id": video_id,
    #     "text": transcript["text"],
    #     "regular_url": f"https://www.youtube.com/watch?v={video_id}",
    #     "url_with_timestamp": f"https://www.youtube.com/watch?v={video_id}&t={transcript['start']}s",
    #     "thumbnail_url": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
    # }
    # for transcript in transcript_dicts
    to_return = []
    for i in range(len(transcript_dicts)):
        combined_text = ""
        regular_url = f"https://www.youtube.com/watch?v={video_id}"
        url_with_timestamp = f"https://www.youtube.com/watch?v={video_id}&t={transcript_dicts[i]['start']}s"
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        for j in range(i, min(i + 20, len(transcript_dicts))):
            combined_text += transcript_dicts[j]["text"] + " "

        to_return.append(
            {
                "id": video_id,
                "text": combined_text.strip(),
                "regular_url": regular_url,
                "url_with_timestamp": url_with_timestamp,
                "thumbnail_url": thumbnail_url,
            }
        )

    return {"transcripts": to_return}
