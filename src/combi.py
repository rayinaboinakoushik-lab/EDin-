"""
Structured and modular YouTube transcript processing script.
Each task is isolated into functions for clarity and maintainability.
"""

import json
import os
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound
)

# --------------------------------------------------
# Load videos from JSON
# --------------------------------------------------
def load_videos(file_path: str):
    """Load video list from a JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# --------------------------------------------------
# Ensure output directory exists
# --------------------------------------------------
def ensure_output_folder(folder: str = "data"):
    """Create folder if it doesn't already exist."""
    os.makedirs(folder, exist_ok=True)

# --------------------------------------------------
# Try fetching transcript for a video using language priority
# --------------------------------------------------
def fetch_transcript(video_id: str, language_order: list):
    """Attempt to fetch a transcript in preferred language order."""
    yt = YouTubeTranscriptApi()

    for lang in language_order:
        try:
            transcript = yt.fetch(video_id, languages=[lang])
            chunks = [part.text for part in transcript]

            return {
                "video_id": video_id,
                "language": lang,
                "transcript_chunks": chunks,
                "full_text": " ".join(chunks)
            }

        except (TranscriptsDisabled, NoTranscriptFound):
            # Try next language
            continue

    # If no transcript was found
    return {
        "video_id": video_id,
        "language": None,
        "transcript_chunks": [],
        "full_text": ""
    }

# --------------------------------------------------
# Save one video's transcript to JSON
# --------------------------------------------------
def save_transcript(video_data: dict, output_folder: str = "data"):
    """Save transcript data for a video to a JSON file."""
    file_path = f"{output_folder}/{video_data['video_id']}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(video_data, f, ensure_ascii=False, indent=4)
    return file_path

# --------------------------------------------------
# Merge multiple transcript outputs into one dataset
# --------------------------------------------------
def merge_transcripts(transcript_list: list):
    """Combine all transcripts into one merged dataset."""
    combined_chunks = []
    combined_full_text = ""

    for data in transcript_list:
        combined_chunks.extend(data["transcript_chunks"])
        combined_full_text += " " + data["full_text"]

    return {
        "total_videos": len(transcript_list),
        "combined_chunks": combined_chunks,
        "combined_text": combined_full_text.strip()
    }

# --------------------------------------------------
# Save merged dataset
# --------------------------------------------------
def save_merged_dataset(merged_data: dict, output_folder: str = "data"):
    """Save merged transcript dataset as JSON."""
    file_path = f"{output_folder}/combined_dataset.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)
    return file_path

# --------------------------------------------------
# Main workflow function
# --------------------------------------------------
def process_transcripts(video_file: str, limit: int = 5, language_order=None):
    """
    Main orchestration function:
    - loads videos
    - fetches transcripts
    - saves individual outputs
    - merges them into a final dataset
    """

    if language_order is None:
        language_order = ["en", "te", "hi"]

    ensure_output_folder("data")

    # 🔴 FUNCTION CALL 🔴  # Calling load_videos(video_file): loads list of videos
    videos = load_videos(video_file)[:limit]

    all_transcripts = []

    for vid in videos:
        video_id = vid["video_id"]
        print(f"Processing: {video_id}")

        # 🔴 FUNCTION CALL 🔴  # Calling fetch_transcript(video_id, language_order): tries to fetch transcript in preferred languages
        transcript_data = fetch_transcript(video_id, language_order)

        # 🔴 FUNCTION CALL 🔴  # Calling save_transcript(transcript_data): saves transcript JSON for one video
        save_transcript(transcript_data)

        all_transcripts.append(transcript_data)

    # 🔴 FUNCTION CALL 🔴  # Calling merge_transcripts(all_transcripts): merges all transcripts into one dataset
    merged = merge_transcripts(all_transcripts)

    # 🔴 FUNCTION CALL 🔴  # Calling save_merged_dataset(merged): saves final combined JSON dataset
    save_merged_dataset(merged)

    print("All transcripts processed successfully.")

# --------------------------------------------------
# Execute if run directly
# --------------------------------------------------
# 🔴 FUNCTION CALL 🔴  # Calling process_transcripts("videos.json", limit=5): main workflow starts here
if __name__ == "__main__":
    process_transcripts("videos.json", limit=5)