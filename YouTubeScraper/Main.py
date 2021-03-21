from YouTubeScraperApi import YouTubeScrapper
from datetime import datetime
import isodate


# ------------------------------------------------------------------------------------------------
#  Удаление ненужных колонок с данными
# ------------------------------------------------------------------------------------------------
def deleteUselessColumns(data):
    # del dataset['video_id']
    del data['playlist_id']


# ------------------------------------------------------------------------------------------------
# Преобразование длительности видео из формата iso8061 в секунды
# ------------------------------------------------------------------------------------------------
def formatDuration(data):
    data['Длительность'] = data['Длительность'].map(lambda date: isodate.parse_duration(date).total_seconds())


# ------------------------------------------------------------------------------------------------
def main():
    channels = ['UCdKuE7a2QZeHPhDntXVZ91w', 'UCQBEHg0j6baNS1Lya-L4BJw', 'UCf31Gf5nCU8J6eUlr7QSU0w',
                'UC-lHJZR3Gqxm24_Vd_AJ5Yw', 'UC7_YxT-KID8kRbqZo7MyscQ',
                'UCIupfj3rki6dfjQqFKbXzMA', 'UC7wgf7YAEMvh7-BStvlBZEg']

    # Получение данных о видео из плейлистов каналов
    for channel in channels:
        ys = YouTubeScrapper(channel)
        data = ys.getAllVideosInfo()
        channelTitle = ys.getChannelTitle()

        # Предобработка данных
        deleteUselessColumns(data)
        formatDuration(data)
        data = data.drop_duplicates(subset=['Название', 'Дата публикации', 'Просмотры', 'Лайки'], keep='first')
        data = data.set_index('video_id')

        # Запись данных в CSV файл
        data.to_csv('dataset/' + channelTitle + ' ' + datetime.strftime(datetime.now(), "%m.%d.%Y") + '.csv',
                    sep=';',
                    encoding='utf_16'
                    )


if __name__ == "__main__":
    main()

# UC8M5YVWQan_3Elm-URehz9w - Топа
# UCdKuE7a2QZeHPhDntXVZ91w - Куплинов
# UCDaIW2zPRWhzQ9Hj7a0QP1w - Усачев
# UCu-__sHtOJpcjKoeJ60LoSA - Черный кабинет
# UCrFiA0hztL9e8zTi_qBuW4w - EoneGay
# UCf31Gf5nCU8J6eUlr7QSU0w - Мармок
# UCQBEHg0j6baNS1Lya-L4BJw - Black Silver
# UC-lHJZR3Gqxm24_Vd_AJ5Yw - Пьюди
# UC7_YxT-KID8kRbqZo7MyscQ - Маркоплаер
