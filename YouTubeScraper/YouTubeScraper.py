from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from time import sleep
from pprint import pprint
import re

import requests
from bs4 import BeautifulSoup


class YouTubeScraper:

    def __init__(self, channel):
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.driver.maximize_window()
        self.channel = channel

    # ------------------------------------------------------------------------------------------------------------------
    # Возвращает все ссылки на плейлисты канала self.channel и Заголовки этих плейлистов в виде двумерного массива
    # ------------------------------------------------------------------------------------------------------------------
    def get_all_playlists_links(self):
        self.driver.get("https://www.youtube.com/channel/" + self.channel + "/playlists?view=1&sort=dd&shelf_id=0")
        self.__scroll_page_to_bottom()
        a_tags = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.LINK_TEXT, 'ПОСМОТРЕТЬ ВЕСЬ ПЛЕЙЛИСТ'))
        )
        titles_elements = self.driver.find_elements_by_css_selector('#video-title')
        links_titles = [[], []]
        for i in range(len(a_tags)):
            links_titles[0].append(a_tags[i].get_attribute('href'))
            links_titles[1].append(titles_elements[i].text)
        return links_titles

    # ------------------------------------------------------------------------------------------------------------------
    # Метод скроллит текущую страницу вниз до конца
    # ------------------------------------------------------------------------------------------------------------------
    def __scroll_page_to_bottom(self):
        load_pause = 1  # Пауза в сек для подгрузки данных
        last_height = self.driver.execute_script("return window.scrollY;")
        while True:
            self.driver.execute_script("window.scrollBy(0, " + str(8000) + ");")
            sleep(load_pause)
            new_height = self.driver.execute_script("return window.scrollY;")
            if new_height == last_height:
                break
            else:
                last_height = new_height

    # ------------------------------------------------------------------------------------------------------------------
    #           *** Метод реализованный через библиотеку Selenium ***
    # Возвращает ссылки на видео из плейлиста и ссылку на плейлист к каждому видео, в виде двумерного массива
    #
    # Parameters:
    #
    # playlist_href - Ссылка на плейлист
    # ------------------------------------------------------------------------------------------------------------------
    def get_all_videos_links(self, playlist_href):
        self.driver.get(playlist_href)
        titles = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#video-title'))
        )
        videos = [[], []]
        for video in titles:
            videos[0].append(video.get_attribute('href'))
            videos[1].append(playlist_href)

        return videos

    # ------------------------------------------------------------------------------------------------------------------
    #           *** Метод реализованный через регулярные выражения и библиотеку Request ***
    # Возвращает ссылки на видео из плейлиста и ссылку на плейлист к каждому видео, в виде двумерного массива
    #
    # Parameters:
    #
    # playlist_href - Ссылка на плейлист
    # ------------------------------------------------------------------------------------------------------------------
    def get_all_videos_links_request(self, playlist_href):
        response_text = requests.get(playlist_href).text
        videos_id = re.findall(r'playlistVideoRenderer":\{"videoId":"[\w,\-,_]+"', response_text)
        videos = [[], []]
        for videos_str in videos_id:
            videos_str = videos_str.replace('playlistVideoRenderer":{"videoId":"', '')
            videos_str = videos_str.replace('"', '')
            videos[0].append('https://www.youtube.com/watch?v=' + videos_str)
            videos[1].append(playlist_href)
        return videos

    # ------------------------------------------------------------------------------------------------------------------
    # Возвращает строку таблицы с информацией по видео
    #
    # Parameters:
    #
    # video_link - Ссылка на видео
    # ------------------------------------------------------------------------------------------------------------------
    def get_all_video_data(self, video_link):
        self.driver.get(video_link)
        return[]

    # ------------------------------------------------------------------------------------------------------------------
    # Возвращает DataFrame со всей нужной инофрмацией о видео на канале
    # ------------------------------------------------------------------------------------------------------------------
    def get_all_videos_info(self):
        # Получение таблицы |playlist_link | playlist_title|
        playlists_info = self.get_all_playlists_links()

        # Получение таблицы |video_link | playlist_link|
        videos_pl_links = [[], []]
        for playlist in playlists_info[0]:
            tmp = self.get_all_videos_links_request(playlist)
            videos_pl_links[0] += tmp[0]
            videos_pl_links[1] += tmp[1]
        pprint(len(videos_pl_links[0]))

        # Получение таблицы |video_link | ... | dislikes | likes | duration|
        videos_info = []
        for video_link in videos_pl_links[0]:
            videos_info += self.get_all_video_data(video_link)

        pprint(videos_info)
        self.driver.close()

# ----------------------------------------------------------------------------------------------------------------------
def main():
    ys = YouTubeScraper('UC8M5YVWQan_3Elm-URehz9w')
    ys.get_all_videos_info()


if __name__ == '__main__':
    main()

# UCyxifPm6ErHW08oXMpzqATw - TNT
# UCdKuE7a2QZeHPhDntXVZ91w - Куплинов
# UC8M5YVWQan_3Elm-URehz9w - Utopia Show
