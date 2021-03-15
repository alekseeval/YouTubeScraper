# TODO: Разобраться с отображением информации для последующей записи
# TODO: Рефакторинг названий переменных (Например playlist_id на самом деле кортеж еще и из title'а)

import googleapiclient as gc
from googleapiclient.discovery import build

import numpy as np
import pandas as pd
from pprint import pprint

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
    # Метод возвращает таблицу, содержащую в себе id плейлиста
    # и его название
    #--------------------------------------------------------------------
    def getAllPlayListsFromChannel(self):
        # Запрос на получение 50 плейлистов канала
        request = self.youtube.playlists().list(
            part        = "snippet",
            channelId   = self.channel_id,
            maxResults  = 50
        )
        response = request.execute()    
        # Заполнение таблицы
        id_title_table = []
        for item in response.get('items'):
            id_title_table.append([item.get('id'), item.get('snippet').get('title')])
        # Если плейлистов больше 50, то необходиом перейти
        # на следующую страницу запроса
        if ('nextPageToken' in response):
            self.__getAllPlayListsFromChannelPage(
                response.get('nextPageToken'), 
                id_title_table
            )
        return id_title_table

    #--------------------------------------------------------------------
    # Вспомогательный метод, аналогичный getAllPlayListsFromChannel 
    # Необходим для перехода на следующую страницу запроса
    #--------------------------------------------------------------------
    def __getAllPlayListsFromChannelPage(self, nextPageToken, id_title_table):
        request = self.youtube.playlists().list(
            part        = "snippet",
            channelId   = self.channel_id,
            maxResults  = 50,
            pageToken   = nextPageToken
        )
        response = request.execute()
        for item in response.get('items'):
            id_title_table.append([item.get('id'), item.get('snippet').get('title')])
        if ('nextPageToken' in response):
            self.__getAllPlayListsFromChannelPage(
                response.get('nextPageToken'), 
                id_title_table
            )

    #--------------------------------------------------------------------
    # Метод возвращает таблицу, содержащую в себе id видео и id плейлиста,
    # в котором находится соответствующее видео
    #
    # Parameters:
    #
    # playlists - id плейлиста, из которого получаем данные
    #--------------------------------------------------------------------
    def getAllPlaylistItems(self, playlist):
        request = self.youtube.playlistItems().list(
            part        ="id, contentDetails",
            maxResults  =50,
            playlistId  =playlist
        )
        response = request.execute()
        video_playlist_table = []
        for item in response.get('items'):
            video_playlist_table.append([item.get('contentDetails').get('videoId'), playlist])
        if ('nextPageToken' in response):
            self.__getAllPlaylistItemsPage(
                playlist, 
                response.get('nextPageToken'), 
                video_playlist_table
            )
        return video_playlist_table

    #--------------------------------------------------------------------
    # Вспомогательный метод, который аналогичен getAllPlaylistItems, 
    # но позволяет перемещаться по страницам запроса
    #--------------------------------------------------------------------
    def __getAllPlaylistItemsPage(self, playlist, nextPageToken, video_playlist_table):
        request = self.youtube.playlistItems().list(
            part        ="id, contentDetails",
            maxResults  =50,
            playlistId  =playlist,
            pageToken   =nextPageToken
        )
        response = request.execute()
        for item in response.get('items'):
            video_playlist_table.append([item.get('contentDetails').get('videoId'), playlist])
        if ('nextPageToken' in response):
            self.__getAllPlaylistItemsPage(
                playlist, 
                response.get('nextPageToken'), 
                video_playlist_table
            )

    #--------------------------------------------------------------------
    # Получение необходимой информации о видео, связанной только с video API
    #--------------------------------------------------------------------
    def __getVideosData(self, videos):
        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=",".join(videos)
        )
        response = request.execute()
        data = []
        for video in response.get('items'):
            cur_data = []
            cur_data.append(video.get('id'))
            snippet = video.get('snippet')
            cur_data.append(snippet.get('title'))
            cur_data.append(snippet.get('publishedAt'))
            statistics = video.get('statistics')
            cur_data += statistics.values()
            cur_data.append(video.get('contentDetails').get('duration'))

            data.append(cur_data)
        return data

    #--------------------------------------------------------------------
    # Получение всей необходимой информации обо всех видео канала
    #--------------------------------------------------------------------
    def getAllVideosInfo(self):
        playlist_ids_titles = np.array(self.getAllPlayListsFromChannel())
        pl_ids_titles = pd.DataFrame(playlist_ids_titles, columns=['playlist_id', 'playlist_title'])

        video_playlist_table = []
        for playlist in playlist_ids_titles[:,0]:
            video_playlist_table += self.getAllPlaylistItems(playlist)
        video_playlist_table = np.array(video_playlist_table)
        video_pl_table = pd.DataFrame(video_playlist_table, columns=['video_id', 'playlist_id'])
        pprint(video_pl_table)
        
        videos = video_playlist_table[:,0]
        videos = [videos[i:i+50] for i in range(0,len(videos),50)]
        videos_data = []
        for videos50 in videos:
            videos_data += self.__getVideosData(videos50)
        videos_data = np.array(videos_data)
        videos_data = pd.DataFrame(
            videos_data, 
            columns=['video_id', 'title', 'publishedDate', 'views', 'likes', 'dislikes', 'favorites', 'comments', 'duration']
        )

#--------------------------------------------------------------------
# Получение необходимых данных
#--------------------------------------------------------------------
ys = YouTubeScrapper("UC8M5YVWQan_3Elm-URehz9w")
ys.getAllVideosInfo()


# PLRYgdCIHj6HVrFlC1FC-TuLTuMn1LkgQg - Топ Сикрет