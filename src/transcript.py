from youtube_transcript_api import YouTubeTranscriptApi
import json

VIDEO_ID = "LR57icC7BFQ"

try:
    yt = YouTubeTranscriptApi()

    transcript = yt.fetch(VIDEO_ID, languages=['te'])

    # Print each caption line
    for part in transcript:
        print(part.text)

    # Save to JSON
    data = {
        "video_id": VIDEO_ID,
        "transcript_chunks": [part.text for part in transcript],
        "full_text": " ".join([part.text for part in transcript])
    } 

    with open("transcript.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("\nTranscript saved.")

except Exception as e:
    print("Transcript unavailable:", e)
