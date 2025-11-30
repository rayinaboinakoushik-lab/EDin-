import requests

API_KEY="AIzaSyCxMe6U4W5ovKLclyQgjm-iB9Gx3ZolIV0"
CHANNEL_ID="UCmeSC2WkskoLgOV5aVGlRrg"

url = (
    "https://www.googleapis.com/youtube/v3/search"
    f"?key={API_KEY}&channelId={CHANNEL_ID}&part=snippet&order=date&maxResults=5"
)
response=requests.get(url)
data=response.json()

for item in data["items"]:
    video_id = item["id"].get("videoId")
    title = item["snippet"]["title"]
    published_at = item["snippet"]["publishedAt"]
    print(video_id, title, published_at)
    
    import json

videos_list = []

for item in data["items"]:
    video_id = item["id"].get("videoId")
    title = item["snippet"]["title"]
    published_at = item["snippet"]["publishedAt"]
    videos_list.append({
        "video_id": video_id,
        "title": title,
        "published_at": published_at 
    })

# Save to data folder (make sure 'data' folder exists)
with open("videos.json", "w", encoding="utf-8") as f:
    json.dump(videos_list, f, ensure_ascii=False, indent=4)

print("Videos saved to ../data/videos.json")
