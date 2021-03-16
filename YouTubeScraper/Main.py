from YouTubeScraperApi import YouTubeScrapper

import pandas as pd
import numpy as np
from pprint import pprint

def main():
    ys = YouTubeScrapper("UC8M5YVWQan_3Elm-URehz9w")
    data = ys.getAllVideosInfo()
    pprint(data)

if __name__ == "__main__":
    main()