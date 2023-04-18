import json
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

from settings import ENV_FILE

load_dotenv(ENV_FILE)


class Video:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=self.video_id
                                                         ).execute()
        self.video_title = self.video_response['items'][0]['snippet']['title']
        self.view_count = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count = self.video_response['items'][0]['statistics']['likeCount']
        self.video_url = f'https://www.youtube.com/watch?v={self.video_id}'

    def print_video_info(self):
        """Выводит в консоль информацию о видео."""
        print(json.dumps(self.video_response, indent=2, ensure_ascii=False))

    def __str__(self):
        return f"{self.video_title}"


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.video_url = f'https://www.youtube.com/watch?v={self.video_id}{self.playlist_id}'
