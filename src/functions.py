import json
import os
def load_videos(file_path):
    with open(file_path,'r') as f:
        return json.load(f)
    
vid =  load_videos("videos.json")
for v in vid:
 
 print(v["video_id"])
 
def create_folder(foldername):
 os.makedirs(foldername, exist_ok=True)

create_folder("5videos")

from youtube_transcript_api import YouTubeTranscriptApi,TranscriptsDisabled,NoTranscriptFound 
yt=YouTubeTranscriptApi()
def fetch_transcript(video_id, language=['en','te','hi']): 
    for lang in language:
        try:
            transcript = yt.fetch(video_id, languages=[lang])
            chunks = [part.text for part in transcript]
            full_text = " ".join([part.text for part in transcript])

            return {
                "video_id": video_id,
                "language": lang,
                "transcript_chunks": chunks,
                "full_text": full_text
            }

        except (TranscriptsDisabled, NoTranscriptFound):
            continue

    # If nothing matched after loop finishes
    return {
        "video_id": video_id,
        "language": None,
        "transcript_chunks": [],
        "full_text": ""
    }
print(fetch_transcript("LR57icC7BFQ"))