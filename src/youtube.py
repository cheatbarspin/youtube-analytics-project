import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

from settings import ENV_FILE

load_dotenv(ENV_FILE)


class YouTube:
    """Специальный класс для работы с API ютуба"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    @classmethod
    def channel(cls, channel_id):
        """Получает данные о канале по его id"""
        return cls.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

    @classmethod
    def video_response(cls, video_id):
        """Получает данные о видео по его id"""
        return cls.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                         id=video_id
                                         ).execute()

    @classmethod
    def playlist_response(cls, playlist_id):
        """Получает данные о плейлисте по его id"""
        return cls.youtube.playlists().list(id=playlist_id,
                                            part='contentDetails, snippet',
                                            maxResults=50,
                                            ).execute()

    @classmethod
    def playlist_videos(cls, playlist_id):
        """Получает данные по видеороликам в плейлисте"""
        return cls.youtube.playlistItems().list(playlistId=playlist_id,
                                                part='contentDetails',
                                                maxResults=50,
                                                ).execute()

    @classmethod
    def video_ids(cls, playlist_id):
        """Метод для получения id видео и добавления их в список"""
        video_ids = []
        for item in cls.playlist_videos(playlist_id)['items']:
            video_ids.append(item['contentDetails']['videoId'])
        return video_ids

    @classmethod
    def video_duration(cls, video_ids):
        """Метод для получения длительности роликов из плейлиста"""
        return cls.youtube.videos().list(part='contentDetails,statistics',
                                         id=','.join(video_ids)
                                         ).execute()
