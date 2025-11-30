import json
import os
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

# Load list of videos
with open("videos.json", "r", encoding="utf-8") as f:
    videos = json.load(f)

# Create output folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# Fetch only first 5 videos
videos_to_process = videos[:5]

# Languages to try in order
LANGS = ['en', 'te', 'hi']  # English → Telugu → Hindi

yt = YouTubeTranscriptApi()  # instance required for your version

for video in videos_to_process:
    video_id = video["video_id"]
    print(f"\n🔍 Fetching transcript for: {video_id}")

    transcript_data = None

    # Try languages one by one
    for lang in LANGS:
        try:
            transcript = yt.fetch(video_id, languages=[lang])
            print(f"✔ Found transcript in: {lang}")

            transcript_data = {
                "video_id": video_id,
                "language": lang,
                "transcript_chunks": [part.text for part in transcript],
                "full_text": " ".join([part.text for part in transcript])
            }
            break

        except (TranscriptsDisabled, NoTranscriptFound):
            print(f"✖ No transcript in: {lang}")

    # If still none found
    if transcript_data is None:
        print(f"⛔ No transcript available for: {video_id}")
        transcript_data = {
            "video_id": video_id,
            "language": None,
            "transcript_chunks": [],
            "full_text": ""
        }

    # Save file
    out_path = f"data/{video_id}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(transcript_data, f, ensure_ascii=False, indent=4)

    print(f"💾 Saved: {out_path}")
