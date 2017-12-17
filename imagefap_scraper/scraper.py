#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The scraper logic.
"""
import os
from multiprocessing import Pool
from functools import partial
from utils import (picture_urls_from_gallery_url,
                   picture_dl_url_from_picture_url, 
                   information_from_picture_dl_url,
                   gallery_title,
                   download_image)

def scrape_picture(picture_url, save_location, ids, verbose, gallery_name):
    """
    Scrape a single picture.
    
    Parameters
    ----------
    
    - picture_url (str): The URL of the picture to save, e.g.
      `http://www.imagefap.com/photo/361343809/?pgid=&gid=7225770&page=0&idx=2`.
      
    - save_location (str): The location to save to, e.g. `downloads`.
    
    - gallery_name (str): Gallery name used for the save folder.
        
    - ids (boolean): Whether or not to use IDs for gallery and picture names.
    
    - verbose (boolean): Whether or not to print information.
    
    
    """

    # Get the download url
    picture_dl_url = picture_dl_url_from_picture_url(picture_url)
    
    # Get information for saving
    username, gallery_id, picture_id, picture_name_full, filetype = \
    information_from_picture_dl_url(picture_dl_url)
    
    # Choose a directory name to save to, 
    # either using gallery ids or gallery name
    if ids:
        save_directory = os.path.join(save_location, gallery_id)
    else:
        save_directory = os.path.join(save_location, gallery_name)
        
    # Create the directory if it does not exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    # Save images
    if ids:
        save_directory = os.path.join(save_directory, picture_id + '.' + filetype)
    else:
        save_directory = os.path.join(save_directory, picture_name_full)
        
    # Download the image
    download_image(picture_dl_url, save_directory)

    if verbose:
        print('Downloaded:', save_directory)

def scrape_gallery(gallery_url, save_location = 'downloads', ids = False,
                   verbose = False, parallel = False):
    """
    Scrape a single gallery.
    
    Parameters
    ----------
    
    - gallery_url (str): The URL of the gallery, e.g.
      `http://www.imagefap.com/gallery.php?gid=7225724?view=2`.
      
    - save_location (str): The location to save to, e.g. `downloads`.
    
    - ids (boolean): Whether or not to use IDs for gallery and picture names.
        
    - verbose (boolean): Whether or not to print information.
    
    - parallel (boolean): Whether or not to use the `multiprocessing` module.
    """
    
    # If a save location is not set, use a folder named `downloads`
    if not save_location:
        save_location = 'downloads'
        
    # Get the name of the gallery, used for the folder to store images in
    gallery_name = gallery_title(gallery_url)
    
    # ------------------------------------------------------------------------
    # If not parallel, do each image sequentially
    if not parallel:
        # Iterate over every picture
        for picture_url in picture_urls_from_gallery_url(gallery_url):
            scrape_picture(picture_url, save_location, 
                           ids, verbose, gallery_name)
            
    # ------------------------------------------------------------------------
    # If parallel, use the `multiprocessing` module
    # This gives a relatively good speedup
    if parallel:
        
        # Create a partial function, i.e. "fill in" some arguments
        scrape_part = partial(scrape_picture, save_location = save_location, 
                              ids = ids, verbose = verbose, 
                              gallery_name = gallery_name)
        
        # Use a Pool with 16 processes in parallel
        with Pool(processes = 16) as pool:
            pool.map(scrape_part, picture_urls_from_gallery_url(gallery_url))
        
        
def main():
    pass


if __name__ == '__main__':
    main()
