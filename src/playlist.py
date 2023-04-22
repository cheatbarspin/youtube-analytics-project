import datetime
import operator
import os
from functools import reduce

from dotenv import load_dotenv
from googleapiclient.discovery import build

from settings import ENV_FILE
from src.video import Video
from src.youtube import YouTube

load_dotenv(ENV_FILE)


class PlayList:
    """Класс для плейлиста"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        """Экземпляр инициализируется id плейлиста. Дальше все данные будут подтягиваться по API."""
        self.playlist_id = playlist_id
        self.playlist_videos = YouTube.playlist_response(playlist_id)
        self.title = self.playlist_videos['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.playlist_videos_2 = YouTube.playlist_videos(playlist_id)
        self.video_ids = YouTube.video_ids(self.playlist_id)

    def get_videos(self):
        """Получает id видео в виде списка"""
        new_list = []
        for video_id in self.video_ids:
            new_list.append(Video(video_id))
        return new_list

    @property
    def total_duration(self) -> datetime.timedelta:
        """Total_duration возвращает объект класса datetime.timedelta
         с суммарной длительность плейлиста
         """
        duration = []
        for video in self.get_videos():
            duration.append(video.get_duration())
        return reduce(operator.add, duration)

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        best_url = ''
        best_videos = int(self.get_videos()[0].like_count)
        for video in self.get_videos():
            if int(video.like_count) > best_videos:
                best_videos = int(video.like_count)
                best_url = video.video_url
        return best_url
