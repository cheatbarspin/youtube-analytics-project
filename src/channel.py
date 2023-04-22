import json
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

from settings import ENV_FILE
from src.youtube import YouTube

load_dotenv(ENV_FILE)


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = YouTube.channel(self.channel_id)
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.channel_id}'
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self):
        """Геттер для id канала"""
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, value):
        """Сеттер на проверку, задан ли атрибут"""
        raise AttributeError("property error")

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    def to_json(self, filename):
        """Записывает в файл формата json информацию о канале"""
        our_dict = self.__dict__
        del our_dict['channel']
        with open(filename, 'w') as file:
            json.dump(our_dict, file, indent=2, ensure_ascii=False)

    def __str__(self):
        """Выводит название и url"""
        return f"{self.title} - {self.url}"

    def __add__(self, other):
        """Магический метод сложения(в данном случае подписчиков 1-го и 2-го"""
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """Магический метод вычитания(в данном случае подписчиков 1-го и 2-го"""
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        """Магический метод сравнения-больше- (в данном случае подписчиков 1-го и 2-го"""
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        """Магический метод сравнения-больше или равно- (в данном случае подписчиков 1-го и 2-го"""
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        """Магический метод сравнения-меньше- (в данном случае подписчиков 1-го и 2-го"""
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        """Магический метод сравнения-меньше или равно- (в данном случае подписчиков 1-го и 2-го"""
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        """Магический метод сравнения-равно- (в данном случае подписчиков 1-го и 2-го"""
        return int(self.subscriber_count) == int(other.subscriber_count)
