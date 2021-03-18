from YouTubeScraperApi import YouTubeScrapper
import isodate


# ------------------------------------------------------------------------------------------------
#  Удаление ненужных колонок с данными
# ------------------------------------------------------------------------------------------------
def deleteUselessColumns(data):
    del data['video_id']
    del data['playlist_id']


# ------------------------------------------------------------------------------------------------
# Преобразование длительности видео из формата iso8061 в секунды
# ------------------------------------------------------------------------------------------------
def formatDuration(data):
    data['duration'] = data['duration'].map(lambda date: isodate.parse_duration(date).total_seconds())


# ------------------------------------------------------------------------------------------------
def main():
    # Получение данных о видео с канала
    ys = YouTubeScrapper("UC8M5YVWQan_3Elm-URehz9w")
    data = ys.getAllVideosInfo()
    channelTitle = ys.getChannelTitle()

    # Предобработка данных
    deleteUselessColumns(data)
    formatDuration(data)

    # Запись данных в CSV файл
    data.to_csv('data/' + channelTitle + '.csv',
                sep=',',
                encoding='utf_16'
                )


if __name__ == "__main__":
    main()

# UC8M5YVWQan_3Elm-URehz9w - Топа
# UCdKuE7a2QZeHPhDntXVZ91w - Куплинов
# UCDaIW2zPRWhzQ9Hj7a0QP1w - Усачев
