import argparse
import csv
import json
import time
import requests
from bs4 import BeautifulSoup


def parse_cents(text):
    """Turn text like '$12.50 to $18.00' into 1250 (cents, as an integer)."""
    text = text.replace(',', '')
    start = text.find('$')
    if start == -1:
        return None
    amount = text[start + 1:].split()[0]
    if '.' in amount:
        dollars, cents = amount.split('.')
        cents = (cents + '0')[:2]
    else:
        dollars, cents = amount, '0'
    return int(dollars) * 100 + int(cents)


def get_text(card, selector):
    """Return the text inside the first matching tag, or None if it isn't there."""
    tag = card.select_one(selector)
    return tag.get_text(' ', strip=True) if tag else None


def download_page(search, page_number):
    response = requests.get(
        'https://www.ebay.com/sch/i.html',
        params={'_nkw': search, '_pgn': page_number},
        headers={'User-Agent': 'Mozilla/5.0'},
        timeout=10,
    )
    response.raise_for_status()
    return response.text


def read_saved_page(pages_dir, page_number):
    with open(f'{pages_dir}/page-{page_number}.html', encoding='utf-8') as f:
        return f.read()


def extract_items(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = []
    for card in soup.select('.s-item'):
        name = get_text(card, '.s-item__title')

        price_text = get_text(card, '.s-item__price')
        price = parse_cents(price_text) if price_text else None

        status = get_text(card, '.SECONDARY_INFO')

        shipping_text = get_text(card, '.s-item__shipping')
        if shipping_text is None:
            shipping = None
        elif 'free' in shipping_text.lower():
            shipping = 0
        else:
            shipping = parse_cents(shipping_text)

        returns_text = get_text(card, '.s-item__free-returns')
        if returns_text is None:
            free_returns = None
        else:
            free_returns = 'free returns' in returns_text.lower()

        sold_text = get_text(card, '.s-item__hotness')
        items_sold = None
        if sold_text:
            first_word = sold_text.split()[0].replace(',', '').replace('+', '')
            if first_word.isdigit():
                items_sold = int(first_word)

        items.append({
            'name': name,
            'price': price,
            'status': status,
            'shipping': shipping,
            'free_returns': free_returns,
            'items_sold': items_sold,
        })
    return items


parser = argparse.ArgumentParser(description='Download eBay search results')
parser.add_argument('--search', required=True)
parser.add_argument('--pages-dir')
parser.add_argument('--csv', action='store_true')
args = parser.parse_args()

all_items = []
for page_number in range(1, 11):
    if args.pages_dir:
        html = read_saved_page(args.pages_dir, page_number)
    else:
        html = download_page(args.search, page_number)
        time.sleep(1)

    page_items = extract_items(html)
    print(f'page {page_number}: {len(page_items)} items')
    all_items.extend(page_items)

if args.csv:
    filename = f'{args.search}.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'price', 'status', 'shipping', 'free_returns', 'items_sold'])
        writer.writeheader()
        writer.writerows(all_items)
else:
    filename = f'{args.search}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_items, f, indent=2)

print(f'saved {len(all_items)} items to {filename}')