import datetime
import json
import os

import isodate
from dotenv import load_dotenv
from googleapiclient.discovery import build

from settings import ENV_FILE
from src.youtube import YouTube

load_dotenv(ENV_FILE)


class Video:
    """Класс для Видео"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id
        self.video_response = YouTube.video_response(self.video_id)
        try:
            self.video_title = self.video_response['items'][0]['snippet']['title']
            self.view_count = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count = self.video_response['items'][0]['statistics']['likeCount']
            self.video_url = f'https://youtu.be/{self.video_id}'
        except IndexError:
            self.video_title = None
            self.video_url = None
            self.view_count = None
            self.like_count = None

    def get_duration(self) -> datetime.timedelta:
        """Метод получения длительности одного видео"""
        iso_8601_duration = self.video_response['items'][0]['contentDetails']['duration']
        return isodate.parse_duration(iso_8601_duration)

    def print_video_info(self):
        """Выводит в консоль информацию о видео."""
        print(json.dumps(self.video_response, indent=2, ensure_ascii=False))

    def __str__(self):
        """Выводит название видео"""
        return f"{self.video_title}"


class PLVideo(Video):
    """Класс для плейлиста этого видео"""

    def __init__(self, video_id, playlist_id):
        """Экземпляр инициализируется id видео, id плейлиста. Дальше все данные будут подтягиваться из класса Родителя."""
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.video_url = f'https://www.youtube.com/watch?v={self.video_id}{self.playlist_id}'
