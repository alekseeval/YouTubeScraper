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
    # Возвращает все ссылки на плейлисты канала self.channel
    # ------------------------------------------------------------------------------------------------------------------
    def get_all_playlists_links(self):
        self.driver.get("https://www.youtube.com/channel/" + self.channel + "/playlists?view=1&sort=dd&shelf_id=0")
        self.__scroll_page_to_bottom()
        a_tags = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.LINK_TEXT, 'ПОСМОТРЕТЬ ВЕСЬ ПЛЕЙЛИСТ'))
        )
        links = []
        for a in a_tags:
            links.append(a.get_attribute('href'))
        return links

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
    # Возвращает DataFrame со всей нужной инофрмацией о видео на канале
    # ------------------------------------------------------------------------------------------------------------------
    def get_all_videos_info(self):
        playlists_links = self.get_all_playlists_links()

        pprint(playlists_links)
        self.driver.close()

# ----------------------------------------------------------------------------------------------------------------------
def main():
    ys = YouTubeScraper('UCdKuE7a2QZeHPhDntXVZ91w')
    ys.get_all_videos_info()


if __name__ == '__main__':
    main()

# UCyxifPm6ErHW08oXMpzqATw - TNT
# UCdKuE7a2QZeHPhDntXVZ91w - Куплинов
# UC8M5YVWQan_3Elm-URehz9w - Utopia Show
