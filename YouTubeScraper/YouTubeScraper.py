from selenium import webdriver
from pprint import pprint


class YouTubeScraper:

    def __init__(self, channel):
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.channel = channel

    def get_all_playlists_links(self):

        return []

    def get_all_videos_info(self):
        self.driver.get("https://www.youtube.com/channel/" + self.channel + "/playlists?view=1&sort=dd&shelf_id=0")
        playlists_links = self.get_all_playlists_links()

        pprint(playlists_links)
        self.driver.close()


def main():
    ys = YouTubeScraper('UCdKuE7a2QZeHPhDntXVZ91w')
    ys.get_all_videos_info()


if __name__ == '__main__':
    main()

# UCyxifPm6ErHW08oXMpzqATw - TNT
# UCdKuE7a2QZeHPhDntXVZ91w - Куплинов
# UC8M5YVWQan_3Elm-URehz9w - Utopia Show
