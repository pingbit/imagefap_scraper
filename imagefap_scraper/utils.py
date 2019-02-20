#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A small set of utility functions, which are used by the scraper.

 - galleries_from_category_url
 - picture_urls_from_gallery_url
 - picture_dl_url_from_picture_url
 - gallery_title
 - information_from_picture_dl_url
 - download_image
 
"""

from bs4 import BeautifulSoup
from requests import get

DOMAIN = r"http://www.imagefap.com"


def galleries_from_category_url(category_url):
    """
    Given a `category_url` such as 
    `http://www.imagefap.com/pics/2/amateur.php`,
    this function yields gallery urls such as
    `http://www.imagefap.com/gallery.php?gid=7225724?view=2`.
    """

    # Download the HTML and create a Beautifulsoup instance
    soup = BeautifulSoup(get(category_url).text, "lxml")

    # Iterate over all `a` tags
    for url in soup.find_all("a"):

        # If the url is a gallery, yield the url
        # Adding `?view=2` ensures that more images are shown
        if "gallery.php?gid=" in url["href"]:
            gallery_url = DOMAIN + url["href"].strip() + "?view=2"
            yield gallery_url


def picture_urls_from_gallery_url(gallery_url):
    """
    Given a `gallery_url` such as
    `http://www.imagefap.com/gallery.php?gid=7225724?view=2`,
    this function yelds picture urls such as
    `http://www.imagefap.com/photo/1659537044/?pgid=&gid=7225724&page=0&idx=0`.
    """

    # Download the HTML and create a Beautifulsoup instance
    soup = BeautifulSoup(get(gallery_url).text, "lxml")

    next_page = None

    # Iterate over all `a` tags
    for url in soup.find_all("a"):

        # If the url is a picture, yield the url
        if "photo/" in url["href"]:
            picture_url = DOMAIN + url["href"]
            yield picture_url

        if ":: next ::" in url.text:
            next_page = url["href"]

    # Another page was found in the pagination, recursively scrape it
    if next_page is not None:

        # Already on a specified view, only add the page
        if "?gid=" in gallery_url:
            base, _ = gallery_url.split("?")  # Split on args
            yield from picture_urls_from_gallery_url(base + next_page)
        else:
            yield from picture_urls_from_gallery_url(gallery_url + next_page)


def picture_dl_url_from_picture_url(picture_url):
    """
    Given a `picture_url` such as
    `http://www.imagefap.com/photo/1659537044/?pgid=&gid=7225724&page=0&idx=0`,
    this function returns a picture download url such as
    `http://x.imagefapusercontent.com/u/Scatsexpeenewbie/7225724/1659537044/image_20.jpeg`.
    """
    # Download the HTML and create a Beautifulsoup instance
    soup = BeautifulSoup(get(picture_url).text, "lxml")

    # Find the image image `img` tag and return the source
    main_image = soup.find("img", attrs={"id": "mainPhoto"})
    picture_dl_url = main_image["src"]
    return picture_dl_url


def gallery_title(gallery_url):
    """
    Given a `gallery_url` such as
    `http://www.imagefap.com/gallery.php?gid=7225724?view=2`,
    this function returns a title such as
    `Best - Dirty blonde hot naked nude`.
    """

    # Download the HTML and create a Beautifulsoup instance
    soup = BeautifulSoup(get(gallery_url).text, "lxml")

    title = soup.title.text.replace("Porn pics of", "")
    i = title.find("(")
    return title[:i].strip()


def information_from_picture_dl_url(picture_dl_url):
    """
    From a `picture_dl_url` such as
    `http://x.imagefapusercontent.com/u/Scatsexpeenewbie/7225724/1659537044/image_20.jpeg`
    this function returns information in a tuple as
    (username, gallery_id, picture_id, picture_name_full, filetype).
    """
    url_split = picture_dl_url.split("/")
    username = url_split[4]
    gallery_id = url_split[5]
    picture_id = url_split[6]
    picture_name_full = url_split[7]
    filetype = picture_name_full.split(".")[-1]

    return username, gallery_id, picture_id, picture_name_full, filetype


def download_image(picture_dl_url, save_location):
    """
    Downloads a `picture_dl_url` such as
    `http://x.imagefapusercontent.com/u/Scatsexpeenewbie/7225724/1659537044/image_20.jpeg`
    to a location on the computer specificed by `save_location`.
    """

    # Get the response
    response = get(picture_dl_url, stream=True)

    # If the status code is OK
    if response.status_code == 200:
        # Create a new file to write to
        with open(save_location, "wb") as file:
            # Iterate over the reponse and write it to the file
            for chunk in response:
                file.write(chunk)


def main():
    pass


if __name__ == "__main__":
    main()
