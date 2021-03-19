from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from time import sleep
from pprint import pprint


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
    # Возвращает DataFrame со всей нужной инофрмацией о видео на канале
    # ------------------------------------------------------------------------------------------------------------------
    def get_all_videos_info(self):
        playlists_info = self.get_all_playlists_links()
        videos_links = [[], []]
        for playlist in playlists_info[0]:
            tmp = self.get_all_videos_links(playlist)
            videos_links[0] += tmp[0]
            videos_links[1] += tmp[1]

        pprint(str(len(videos_links[0])) + ' - ' + str(len(videos_links[1])))
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
