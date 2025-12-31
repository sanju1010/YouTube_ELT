import requests

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"

def get_playlist_id():
    try:
        url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        return data['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
    print(get_playlist_id())




