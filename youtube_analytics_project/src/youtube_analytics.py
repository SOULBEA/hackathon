# filepath: src/youtube_analytics.py
from googleapiclient.discovery import build

# API setup
YOUTUBE_API_KEY = "AIzaSyDrPUzZ99Ljfxg0FnmncO1qecFSzDV4P58"  # Replace with your YouTube API key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)

def get_channel_details(channel_id):
    request = youtube.channels().list(part="snippet,statistics", id=channel_id)
    response = request.execute()
    if "items" not in response or len(response["items"]) == 0:
        return None
    data = response["items"][0]
    channel_stats = {
        "Title": data["snippet"]["title"],
        "Subscribers": int(data["statistics"]["subscriberCount"]),
        "Total Views": int(data["statistics"]["viewCount"]),
        "Total Videos": int(data["statistics"]["videoCount"]),
    }
    return channel_stats