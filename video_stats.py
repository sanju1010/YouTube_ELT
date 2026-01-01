import json

import requests
import os
from datetime import date

from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"
maxResults = 50

def get_playlist_id():
    try:
        url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        return data['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    except requests.exceptions.RequestException as e:
        raise e

def get_video_ids(play_list_id):
    video_ids = []
    nextPageToken = None
    base_url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId={play_list_id}&key={API_KEY}"
    try:
        while True:
            url = base_url
            if nextPageToken:
                url = url + f"&pageToken={nextPageToken}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            for item in data.get("items", []):
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id)
            nextPageToken = data.get("nextPageToken")
            if not nextPageToken:
                break
        return video_ids
    except requests.exceptions.RequestException as e:
        raise e

def extract_video_data(video_ids):
    extracted_data = []

    def batch_list(video_ids, batch_size):
        for video in range(0, len(video_ids), batch_size):
            yield video_ids[video:video+batch_size]
    try:
        for batch in batch_list(video_ids, maxResults):
            video_ids_str = ",".join(batch)
            url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            for item in data.get("items", []):

                video_id = item["id"]
                snippet = item["snippet"]
                contentDetails = item["contentDetails"]
                statistics = item["statistics"]

                video_data = {
                    "video_id": video_id,
                    "title": snippet["title"],
                    "publishedAt": snippet[ "publishedAt"],
                    "duration": contentDetails["duration"],
                    "viewCount": statistics.get("viewCount", None),
                    "likeCount": statistics.get("likeCount", None),
                    "commentCount": statistics.get("commentCount", None)
                }

                extracted_data.append(video_data)

        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e

def save_to_jason(extracted_data):
    file_path = f"./data/YT_data_{date.today()}.json"
    with open(file_path, "w", encoding="utf-8") as json_output_file:
        json.dump(extracted_data, json_output_file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    play_list_id = get_playlist_id()
    print(f"Play list id:{play_list_id}")
    video_ids = get_video_ids(play_list_id)
    print(f"Total videos:{len(video_ids)}")
    video_data = extract_video_data(video_ids)
    save_to_jason(video_data)




