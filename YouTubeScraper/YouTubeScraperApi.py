# TODO: Разобраться с отображением информации для последующей записи
# TODO: Рефакторинг названий переменных (Например playlist_id на самом деле кортеж еще и из title'а)

import googleapiclient as gc
from googleapiclient.discovery import build

import pandas as pd
import json
import pprint

class YouTubeScrapper:
    #--------------------------------------------------------------------
    # Инициализация параметров, необходимых для работы с API
    #--------------------------------------------------------------------
    DEVELOPER_KEY = "AIzaSyAMxGTzlqpZzkyHSGy1ST0U3NQ-RZ27pss"
    api_service_name = 'youtube'
    api_version = 'v3'
    youtube = build(api_service_name, api_version, developerKey=DEVELOPER_KEY)
    channel_id = "UC8M5YVWQan_3Elm-URehz9w"

    def __init__(self, channel_id):
        self.channel_id = channel_id

    #--------------------------------------------------------------------
    # Метод возвращает список кортежей состоящих из id всех плейлистов
    # и их названий (id, title) для канала
    #--------------------------------------------------------------------
    def getAllPlayListsFromChannel(self):
        # Запрос на получение всех плейлистов канала
        request = self.youtube.playlists().list(
            part        = "snippet",
            channelId   = self.channel_id,
            maxResults  = 50
        )
        response = request.execute()    
        playlists_ids = []
        for item in response.get('items'):
            playlists_ids.append((item.get('id'), item.get('snippet').get('title')))
        if ('nextPageToken' in response):
            self.__getAllPlayListsFromChannelPagee(
                response.get('nextPageToken'), 
                playlist_id
            )
        return playlists_ids

    #--------------------------------------------------------------------
    # Вспомогательный метод, который так же возвращает кортежи, состоящие из 
    # id и title для всех плейлистов канала, но с учетом pagination
    # Метод аналогичен предыдущему, за исключением параметров запроса
    #--------------------------------------------------------------------
    def __getAllPlayListsFromChannelPage(self, nextPageToken, playlists_id):
        request = self.youtube.playlists().list(
            part        = "snippet",
            channelId   = self.channel_id,
            maxResults  = 50,
            pageToken   = nextPageToken
        )
        response = request.execute()
        for item in response.get('items'):
            playlists_ids.append((item.get('id'), item.get('snippet').get('title')))
        if ('nextPageToken' in response):
            self.__getAllPlayListsFromChannelPage(
                response.get('nextPageToken'), 
                playlist_id
            )

    #--------------------------------------------------------------------
    # Метод возвращает id всех видео канала, содержащихся в некотором плейлисте
    #
    # Parameters:
    #
    # playlist_id - id плейлиста, из которого получаем необходимую информацию
    #--------------------------------------------------------------------
    def getAllPlaylistItems(self, playlist_id):
        request = self.youtube.playlistItems().list(
            part        ="id, contentDetails",
            maxResults  =50,
            playlistId  =playlist_id
        )
        response = request.execute()
        videos_id = []
        for item in response.get('items'):
            videos_id.append(item.get('contentDetails').get('videoId'))
        if ('nextPageToken' in response):
            self.__getAllPlaylistItemsFromPage(
                playlist_id, 
                response.get('nextPageToken'), 
                videos_id
            )
        return videos_id

    #--------------------------------------------------------------------
    # Вспомогательный метод, который возвращает id всех видео канала, 
    # с учетом pagination в запросах
    #--------------------------------------------------------------------
    def __getAllPlaylistItemsFromPage(self, playlist_id, nextPageToken, videos_id):
        request = self.youtube.playlistItems().list(
            part        ="id",
            maxResults  =50,
            playlistId  =playlist_id,
            pageToken   =nextPageToken
        )
        response = request.execute()
        for item in response.get('items'):
            videos_id.append(item.get('id'))
        if ('nextPageToken' in response):
            self.__getAllPlaylistItemsFromPage(
                playlist_id, 
                response.get('nextPageToken'), 
                videos_id
            )

    #--------------------------------------------------------------------
    # Получение необходимой информации об отдельном видео 
    #--------------------------------------------------------------------
    def getSingleVideoInfo(self, video_id, playlist_title):
        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()
        return 1

    #--------------------------------------------------------------------
    # Получение всей необходимой информации обо всех видео канала
    #--------------------------------------------------------------------
    def getAllVideosInfo(self):
        playlist_ids = self.getAllPlayListsFromChannel()
        all_videos_id = []
        videos_data = []
        for playlist_id in playlist_ids:
            for video_id in self.getAllPlaylistItems(playlist_id[0]):
                # playlist_id[1]     % Название плейлиста
                videos_data.append(self.getSingleVideoInfo(video_id, playlist_id[1]))
        return videos_data

#--------------------------------------------------------------------
# Получение необходимых данных
#--------------------------------------------------------------------
ys = YouTubeScrapper("UC8M5YVWQan_3Elm-URehz9w")
ys.getAllVideosInfo()


# PLRYgdCIHj6HVrFlC1FC-TuLTuMn1LkgQg - Топ Сикрет