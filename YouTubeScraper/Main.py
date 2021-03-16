from YouTubeScraperApi import YouTubeScrapper

import pandas as pd
import numpy as np
from pprint import pprint
import re

#------------------------------------------------------------------------------------------------
#  Удаление ненужных колонок с данными
#------------------------------------------------------------------------------------------------
def deleteUselessColumns(data):
    del data['video_id']
    del data['playlist_id']

#------------------------------------------------------------------------------------------------
def main():
    #Получение данных о видео с канала
    ys = YouTubeScrapper("UCdKuE7a2QZeHPhDntXVZ91w")
    data = ys.getAllVideosInfo()
    channelTitle = ys.getChannelTitle()

    # Предобработка данных
    deleteUselessColumns(data)

    # Запись данных в CSV файл
    data.to_csv('result/' + channelTitle + '.csv',
              sep=',',
              encoding='utf_16'
              )
    pprint(data.head())

if __name__ == "__main__":
    main()

#UC8M5YVWQan_3Elm-URehz9w - Топа
#UCdKuE7a2QZeHPhDntXVZ91w - Куплинов