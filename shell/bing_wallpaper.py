#!/usr/bin/env python
"""
Downlaods the daily Bing wallpaper to a configured folder.
"""
from os import makedirs
from os.path import expanduser, basename, join
import requests

BASE_URL = 'http://www.bing.com'
WALLPAPER_QUERY = '/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'
DOWNLOAD_PATH = expanduser('~/Pictures/Wallpapers')


def get_wallpaper():
    """Downloads wallpaper."""
    response = requests.get('{}{}'.format(BASE_URL, WALLPAPER_QUERY))
    response.raise_for_status()
    url = response.json()['images'][0]['url']
    try:
        makedirs(DOWNLOAD_PATH)
    except OSError as exc:
        if exc.args[0] != 17:
            raise
            
    wallpaper = requests.get('{}{}'.format(BASE_URL, url), stream=True)
    with open(join(DOWNLOAD_PATH, basename(url)), 'wb') as file_descriptor:
        for chunk in wallpaper.iter_content(chunk_size=128):
            file_descriptor.write(chunk)


if __name__ == '__main__':
    get_wallpaper()
