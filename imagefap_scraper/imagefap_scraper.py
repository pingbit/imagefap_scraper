#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This is the main file for the command line interface of the imagefap
scraper. It takes arguments from the user and passes the arguments
to the correct functions for handling.
"""
from scraper import scrape_gallery
from utils import galleries_from_category_url
import argparse

def parse_args():
    """
    Use the `argparse` module to get arguments from the user.
    """
    
    # Set up constants to be used
    description = 'Download galleries from imagefap.'
    gallery_url_ex = r'http://www.imagefap.com/gallery.php?gid=7225724'
    category_url_ex = r'http://www.imagefap.com/pics/2/amateur.php'
    #save_location_ex = r'downloads'
    
    # Parse the arguments
    parser = argparse.ArgumentParser(description=description)
    
    # Arguments with specified values
    parser.add_argument('--gallery_urls', type=str, nargs='*',
                help='A gallery url such as `{}`.'.format(gallery_url_ex))
    
    parser.add_argument('--category_url', type=str,
                help='A category url such as `{}`.'.format(category_url_ex))
    
    # Deprecated
    #parser.add_argument('--save_location', type=str,
    #            help='A save location such as `{}`.'.format(save_location_ex)) 
    
    # Arguments which are True or False
    constants_args = {'action' : 'store_true', 'default' : False}
    parser.add_argument('-verbose', 
                help='Whether or not to print information.',
                **constants_args)
    
    parser.add_argument('-ids', 
                help='Use picture and gallery IDs, not readable names.',
                **constants_args)
    
    parser.add_argument('-parallel', 
                help='Parallel processing using the `multiprocessing` module.',
                **constants_args) 
    
    arguments = parser.parse_args()
    return arguments
    
    
def process_args(arguments):
    """
    Forward the arguments to the required functions.
    """
    args = arguments
    
    # The user wants to scrape one or more galleries by URL
    if args.gallery_urls:
        for gallery_url in args.gallery_urls:
            scrape_gallery(gallery_url = gallery_url.strip(), 
                           #save_location = args.save_location, 
                           ids = args.ids, verbose = args.verbose,
                           parallel = args.parallel)
            
            
    # The user wants to scrape a category
    if args.category_url:
        for gallery_url in galleries_from_category_url(args.category_url.strip()):
            scrape_gallery(gallery_url = gallery_url.strip(), 
                           #save_location = args.save_location, 
                           ids = args.ids, verbose = args.verbose,
                           parallel = args.parallel)

def main():
    
    # Get the arguments from the user and parse
    arguments = parse_args()
    process_args(arguments)
    
    
if __name__ == '__main__':
    main()
