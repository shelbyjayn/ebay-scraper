# ebay-scraper

`ebay-dl.py` scrapes eBay search results. Given a search term, it downloads the first 10 pages of results with the `requests` library, uses Beautiful Soup to extract each listing's name, price, condition, shipping cost, free returns, and number sold, and saves the listings to a JSON file named after the search term. Prices and shipping are stored in cents as integers, and any field a listing doesn't show is saved as `null`.

## Running ebay-dl.py

Live eBay requests timed out when I ran this, so all three outputs use the artificial practice listings from `practice-pages`. The listings are the same in each file; only the filename comes from the search term.

These commands generate the three JSON files:

```
python ebay-dl.py --search "digital camera" --pages-dir practice-pages
python ebay-dl.py --search "film camera" --pages-dir practice-pages
python ebay-dl.py --search "tripod" --pages-dir practice-pages
```

To download live results from eBay, leave off `--pages-dir`:

```
python ebay-dl.py --search "digital camera"
```

## CSV output (extra credit)

Add `--csv` to save a CSV file instead of JSON. These commands generate the three CSV files:

```
python ebay-dl.py --search "digital camera" --pages-dir practice-pages --csv
python ebay-dl.py --search "film camera" --pages-dir practice-pages --csv
python ebay-dl.py --search "tripod" --pages-dir practice-pages --csv
```

## Project page

[Project 2: Scraping eBay](https://github.com/shelbyjayn/ebay-scraper)