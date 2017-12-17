# imagefap_scraper
A web scraper for imagefap, with features:

- Scraping of single, or multiple, galleries.
- Scraping of every gallery on a category page.
- Parallel scraping of images withing each gallery scraped.
- Storage as human-readable, or using gallery and image `IDs`.

See the examples below for more information.


## Examples

**Example 1)** Download all images from a single gallery. The `-v` argument enables verbose printing, and the `-p` argument enables parallelism.
```
python imagefap_scraper.py --gallery_urls 'http://www.imagefap.com/pictures/123/BLAH-BLAH' -v -p
```

**Example 2)** Download all images from two galleries.
```
python imagefap_scraper.py --gallery_urls 'http://www.imagefap.com/gallery.php?gid=1234' 'http://www.imagefap.com/gallery.php?gid=12345' -v -p
```

**Example 3)** Download all images from a single gallery. The `-ids` argument tells the scraper to name the downloaded gallery and pictures using gallery and picture `ids` instead of human-readable names.
```
python imagefap_scraper.py --gallery_urls 'http://www.imagefap.com/pictures/123/BLAH-BLAH' -v -p -ids
```

## Technical information

- Written using Python 3.6.3.
- Dependencies: `bs4`

### Installation

1. sdf
2. sdf



## Full documentation

```
usage: imagefap_scraper.py 
[-h]
[--gallery_urls GALLERY_URLS [GALLERY_URLS ...]]
[--category_url CATEGORY_URL] [-verbose] [-ids]
[-parallel]

Download galleries from imagefap.

optional arguments:
  -h, --help            show this help message and exit
  --gallery_urls GALLERY_URLS [GALLERY_URLS ...]
                        A gallery url such as
                        `http://www.imagefap.com/gallery.php?gid=7225724`.
  --category_url CATEGORY_URL
                        A category url such as
                        `http://www.imagefap.com/pics/2/amateur.php`.
  -verbose              Whether or not to print information.
  -ids                  Use picture and gallery IDs, not readable names.
  -parallel             Parallel processing using the `multiprocessing`
                        module.
```

