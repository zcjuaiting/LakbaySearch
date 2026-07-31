import json
import os
import time
import re
from typing import Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup, Tag

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DOCUMENTS_PATH = os.path.join(DATA_DIR, "documents.json")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

REQUEST_TIMEOUT = 30
CRAWL_DELAY = 1.5


CURATED_URLS: List[Dict[str, str]] = [
    {"url": "https://beta.tourism.gov.ph/", "source": "tourism.gov.ph", "category": "Other"},
    {"url": "https://beta.tourism.gov.ph/about-dot/", "source": "tourism.gov.ph", "category": "Other"},
    {"url": "https://beta.tourism.gov.ph/tourism-products/", "source": "tourism.gov.ph", "category": "Other"},
    {"url": "https://beta.tourism.gov.ph/tourism-products/beaches-and-diving/", "source": "tourism.gov.ph", "category": "Beaches"},
    {"url": "https://beta.tourism.gov.ph/tourism-products/culture-and-heritage/", "source": "tourism.gov.ph", "category": "Cultural Attractions"},
    {"url": "https://beta.tourism.gov.ph/tourism-products/nature-and-adventure/", "source": "tourism.gov.ph", "category": "Nature"},
    {"url": "https://beta.tourism.gov.ph/tourism-products/mice/", "source": "tourism.gov.ph", "category": "Other"},
    {"url": "https://beta.tourism.gov.ph/tourism-products/sun-and-beach/", "source": "tourism.gov.ph", "category": "Beaches"},
    {"url": "https://beta.tourism.gov.ph/tourism-products/diving/", "source": "tourism.gov.ph", "category": "Beaches"},
    {"url": "https://beta.tourism.gov.ph/tourism-products/eco-tourism/", "source": "tourism.gov.ph", "category": "Nature"},
    {"url": "https://beta.tourism.gov.ph/tourism-products/agri-tourism/", "source": "tourism.gov.ph", "category": "Nature"},
    {"url": "https://beta.tourism.gov.ph/tourism-products/culinary-arts/", "source": "tourism.gov.ph", "category": "Cultural Attractions"},
    {"url": "https://beta.tourism.gov.ph/tourism-products/creative-arts/", "source": "tourism.gov.ph", "category": "Cultural Attractions"},
    {"url": "https://beta.tourism.gov.ph/tourism-products/wellness-and-health/", "source": "tourism.gov.ph", "category": "Other"},
    {"url": "https://beta.tourism.gov.ph/tourism-products/community-based-tourism/", "source": "tourism.gov.ph", "category": "Cultural Attractions"},
    {"url": "https://beta.tourism.gov.ph/news-and-updates/", "source": "tourism.gov.ph", "category": "Other"},
    {"url": "https://beta.tourism.gov.ph/experiences-and-destinations/", "source": "tourism.gov.ph", "category": "Other"},
    {"url": "https://beta.tourism.gov.ph/experiences-and-destinations/boracay/", "source": "tourism.gov.ph", "category": "Beaches"},
    {"url": "https://beta.tourism.gov.ph/experiences-and-destinations/palawan/", "source": "tourism.gov.ph", "category": "Beaches"},
    {"url": "https://beta.tourism.gov.ph/experiences-and-destinations/cebu/", "source": "tourism.gov.ph", "category": "Historical Sites"},
    {"url": "https://beta.tourism.gov.ph/experiences-and-destinations/bohol/", "source": "tourism.gov.ph", "category": "Nature"},
    {"url": "https://beta.tourism.gov.ph/experiences-and-destinations/siargao/", "source": "tourism.gov.ph", "category": "Beaches"},
    {"url": "https://beta.tourism.gov.ph/experiences-and-destinations/baguio/", "source": "tourism.gov.ph", "category": "Cities"},
    {"url": "https://beta.tourism.gov.ph/experiences-and-destinations/davao/", "source": "tourism.gov.ph", "category": "Cities"},
    {"url": "https://beta.tourism.gov.ph/experiences-and-destinations/ilocos-norte/", "source": "tourism.gov.ph", "category": "Historical Sites"},
    {"url": "https://beta.tourism.gov.ph/experiences-and-destinations/ilocos-sur/", "source": "tourism.gov.ph", "category": "Historical Sites"},
    {"url": "https://beta.tourism.gov.ph/experiences-and-destinations/laoag/", "source": "tourism.gov.ph", "category": "Historical Sites"},
    {"url": "https://beta.tourism.gov.ph/experiences-and-destinations/vigan/", "source": "tourism.gov.ph", "category": "Historical Sites"},
    {"url": "https://beta.tourism.gov.ph/experiences-and-destinations/puerto-princesa/", "source": "tourism.gov.ph", "category": "Nature"},
    {"url": "https://beta.tourism.gov.ph/experiences-and-destinations/tagaytay/", "source": "tourism.gov.ph", "category": "Nature"},
    {"url": "https://beta.tourism.gov.ph/experiences-and-destinations/manila/", "source": "tourism.gov.ph", "category": "Cities"},
    {"url": "https://beta.tourism.gov.ph/experiences-and-destinations/makati/", "source": "tourism.gov.ph", "category": "Cities"},
    {"url": "https://beta.tourism.gov.ph/experiences-and-destinations/banaue/", "source": "tourism.gov.ph", "category": "Historical Sites"},
    {"url": "https://beta.tourism.gov.ph/experiences-and-destinations/sagada/", "source": "tourism.gov.ph", "category": "Mountains"},
    {"url": "https://beta.tourism.gov.ph/experiences-and-destinations/coron/", "source": "tourism.gov.ph", "category": "Beaches"},
    {"url": "https://beta.tourism.gov.ph/experiences-and-destinations/el-nido/", "source": "tourism.gov.ph", "category": "Beaches"},
    {"url": "https://en.wikipedia.org/wiki/Philippines", "source": "en.wikipedia.org", "category": "Other"},
    {"url": "https://en.wikipedia.org/wiki/Tourism_in_the_Philippines", "source": "en.wikipedia.org", "category": "Other"},
    {"url": "https://en.wikipedia.org/wiki/Boracay", "source": "en.wikipedia.org", "category": "Beaches"},
    {"url": "https://en.wikipedia.org/wiki/Palawan", "source": "en.wikipedia.org", "category": "Beaches"},
    {"url": "https://en.wikipedia.org/wiki/El_Nido,_Palawan", "source": "en.wikipedia.org", "category": "Beaches"},
    {"url": "https://en.wikipedia.org/wiki/Puerto_Princesa_Subterranean_River_National_Park", "source": "en.wikipedia.org", "category": "Nature"},
    {"url": "https://en.wikipedia.org/wiki/Chocolate_Hills", "source": "en.wikipedia.org", "category": "Nature"},
    {"url": "https://en.wikipedia.org/wiki/Bohol", "source": "en.wikipedia.org", "category": "Nature"},
    {"url": "https://en.wikipedia.org/wiki/Cebu", "source": "en.wikipedia.org", "category": "Cities"},
    {"url": "https://en.wikipedia.org/wiki/Mactan", "source": "en.wikipedia.org", "category": "Beaches"},
    {"url": "https://en.wikipedia.org/wiki/Siargao", "source": "en.wikipedia.org", "category": "Beaches"},
    {"url": "https://en.wikipedia.org/wiki/Baguio", "source": "en.wikipedia.org", "category": "Cities"},
    {"url": "https://en.wikipedia.org/wiki/Davao_City", "source": "en.wikipedia.org", "category": "Cities"},
    {"url": "https://en.wikipedia.org/wiki/Mount_Apo", "source": "en.wikipedia.org", "category": "Mountains"},
    {"url": "https://en.wikipedia.org/wiki/Mount_Mayon", "source": "en.wikipedia.org", "category": "Mountains"},
    {"url": "https://en.wikipedia.org/wiki/Mount_Pinatubo", "source": "en.wikipedia.org", "category": "Mountains"},
    {"url": "https://en.wikipedia.org/wiki/Mount_Taal", "source": "en.wikipedia.org", "category": "Mountains"},
    {"url": "https://en.wikipedia.org/wiki/Taal_Volcano", "source": "en.wikipedia.org", "category": "Nature"},
    {"url": "https://en.wikipedia.org/wiki/Mayon_Volcano", "source": "en.wikipedia.org", "category": "Mountains"},
    {"url": "https://en.wikipedia.org/wiki/Banaue_Rice_Terraces", "source": "en.wikipedia.org", "category": "Historical Sites"},
    {"url": "https://en.wikipedia.org/wiki/Historic_City_of_Vigan", "source": "en.wikipedia.org", "category": "Historical Sites"},
    {"url": "https://en.wikipedia.org/wiki/Intramuros", "source": "en.wikipedia.org", "category": "Historical Sites"},
    {"url": "https://en.wikipedia.org/wiki/Rizal_Park", "source": "en.wikipedia.org", "category": "Historical Sites"},
    {"url": "https://en.wikipedia.org/wiki/Baroque_Churches_of_the_Philippines", "source": "en.wikipedia.org", "category": "Historical Sites"},
    {"url": "https://en.wikipedia.org/wiki/San_Agustin_Church_(Manila)", "source": "en.wikipedia.org", "category": "Historical Sites"},
    {"url": "https://en.wikipedia.org/wiki/Paoay_Church", "source": "en.wikipedia.org", "category": "Historical Sites"},
    {"url": "https://en.wikipedia.org/wiki/Santo_Ni%C3%B1o_Basilica_(Cebu)", "source": "en.wikipedia.org", "category": "Historical Sites"},
    {"url": "https://en.wikipedia.org/wiki/Magellan%27s_Cross", "source": "en.wikipedia.org", "category": "Historical Sites"},
    {"url": "https://en.wikipedia.org/wiki/Fort_San_Pedro", "source": "en.wikipedia.org", "category": "Historical Sites"},
    {"url": "https://en.wikipedia.org/wiki/Coron,_Palawan", "source": "en.wikipedia.org", "category": "Beaches"},
    {"url": "https://en.wikipedia.org/wiki/Tubbataha_Reef", "source": "en.wikipedia.org", "category": "Beaches"},
    {"url": "https://en.wikipedia.org/wiki/Apo_Reef", "source": "en.wikipedia.org", "category": "Beaches"},
    {"url": "https://en.wikipedia.org/wiki/White_Beach_(Boracay)", "source": "en.wikipedia.org", "category": "Beaches"},
    {"url": "https://en.wikipedia.org/wiki/Pagsanjan_Falls", "source": "en.wikipedia.org", "category": "Nature"},
    {"url": "https://en.wikipedia.org/wiki/Kawasan_Falls", "source": "en.wikipedia.org", "category": "Nature"},
    {"url": "https://en.wikipedia.org/wiki/Hundred_Islands_National_Park", "source": "en.wikipedia.org", "category": "Beaches"},
    {"url": "https://en.wikipedia.org/wiki/Manila", "source": "en.wikipedia.org", "category": "Cities"},
    {"url": "https://en.wikipedia.org/wiki/Makati", "source": "en.wikipedia.org", "category": "Cities"},
    {"url": "https://en.wikipedia.org/wiki/Quezon_City", "source": "en.wikipedia.org", "category": "Cities"},
    {"url": "https://en.wikipedia.org/wiki/Tagaytay", "source": "en.wikipedia.org", "category": "Nature"},
    {"url": "https://en.wikipedia.org/wiki/Lake_Taal", "source": "en.wikipedia.org", "category": "Nature"},
    {"url": "https://en.wikipedia.org/wiki/Sagada", "source": "en.wikipedia.org", "category": "Mountains"},
    {"url": "https://en.wikipedia.org/wiki/Ifugao", "source": "en.wikipedia.org", "category": "Historical Sites"},
    {"url": "https://en.wikipedia.org/wiki/Camiguin", "source": "en.wikipedia.org", "category": "Nature"},
    {"url": "https://en.wikipedia.org/wiki/Siquijor", "source": "en.wikipedia.org", "category": "Beaches"},
    {"url": "https://en.wikipedia.org/wiki/Philippine_Cuisine", "source": "en.wikipedia.org", "category": "Cultural Attractions"},
    {"url": "https://en.wikipedia.org/wiki/Ati-Atihan_festival", "source": "en.wikipedia.org", "category": "Cultural Attractions"},
    {"url": "https://en.wikipedia.org/wiki/Sinulog", "source": "en.wikipedia.org", "category": "Cultural Attractions"},
    {"url": "https://en.wikipedia.org/wiki/Pahiyas_Festival", "source": "en.wikipedia.org", "category": "Cultural Attractions"},
    {"url": "https://en.wikipedia.org/wiki/MassKara_Festival", "source": "en.wikipedia.org", "category": "Cultural Attractions"},
    {"url": "https://en.wikipedia.org/wiki/Panagbenga_Festival", "source": "en.wikipedia.org", "category": "Cultural Attractions"},
    {"url": "https://en.wikipedia.org/wiki/List_of_Beaches_in_the_Philippines", "source": "en.wikipedia.org", "category": "Beaches"},
    {"url": "https://en.wikipedia.org/wiki/List_of_national_parks_of_the_Philippines", "source": "en.wikipedia.org", "category": "Nature"},
    {"url": "https://en.wikipedia.org/wiki/National_Museum_of_the_Philippines", "source": "en.wikipedia.org", "category": "Cultural Attractions"},
    {"url": "https://en.wikipedia.org/wiki/Philippine_Eagle", "source": "en.wikipedia.org", "category": "Nature"},
    {"url": "https://en.wikipedia.org/wiki/Tarsier", "source": "en.wikipedia.org", "category": "Nature"},
    {"url": "https://en.wikipedia.org/wiki/Whale_shark", "source": "en.wikipedia.org", "category": "Nature"},
    {"url": "https://en.wikipedia.org/wiki/Anilao", "source": "en.wikipedia.org", "category": "Beaches"},
    {"url": "https://en.wikipedia.org/wiki/Moalboal", "source": "en.wikipedia.org", "category": "Beaches"},
    {"url": "https://en.wikipedia.org/wiki/Dumaguete", "source": "en.wikipedia.org", "category": "Cities"},
    {"url": "https://en.wikipedia.org/wiki/Baler,_Aurora", "source": "en.wikipedia.org", "category": "Beaches"},
    {"url": "https://en.wikipedia.org/wiki/La_Union", "source": "en.wikipedia.org", "category": "Beaches"},
    {"url": "https://en.wikipedia.org/wiki/Subic_Bay", "source": "en.wikipedia.org", "category": "Historical Sites"},
    {"url": "https://en.wikipedia.org/wiki/Corregidor", "source": "en.wikipedia.org", "category": "Historical Sites"},
    {"url": "https://en.wikipedia.org/wiki/Las_Pi%C3%B1as_Bamboo_Organ", "source": "en.wikipedia.org", "category": "Cultural Attractions"},
    {"url": "https://en.wikipedia.org/wiki/Mindanao", "source": "en.wikipedia.org", "category": "Cities"},
    {"url": "https://en.wikipedia.org/wiki/Zamboanga_City", "source": "en.wikipedia.org", "category": "Cities"},
    {"url": "https://en.wikipedia.org/wiki/General_Santos", "source": "en.wikipedia.org", "category": "Cities"},
    {"url": "https://en.wikipedia.org/wiki/Cagayan_de_Oro", "source": "en.wikipedia.org", "category": "Cities"},
    {"url": "https://en.wikipedia.org/wiki/Iloilo_City", "source": "en.wikipedia.org", "category": "Cities"},
    {"url": "https://en.wikipedia.org/wiki/Bacolod", "source": "en.wikipedia.org", "category": "Cities"},
    {"url": "https://en.wikipedia.org/wiki/Puerto_Galera", "source": "en.wikipedia.org", "category": "Beaches"},
]


def extract_dot_content(soup: BeautifulSoup, url: str) -> Tuple[str, str, str]:
    for tag in soup.find_all(['script', 'style', 'nav', 'footer', 'header', 'aside']):
        tag.decompose()

    title = ""
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.get_text(strip=True)

    heading = ""
    h1 = soup.find('h1')
    if h1:
        heading = h1.get_text(strip=True)
    if not heading:
        h2 = soup.find('h2')
        if h2:
            heading = h2.get_text(strip=True)

    content_parts = []
    main = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'(content|main|entry|post|body)'))
    if main:
        for p in main.find_all(['p', 'h2', 'h3', 'h4', 'li', 'span']):
            text = p.get_text(strip=True)
            if text and len(text) > 20:
                content_parts.append(text)
    else:
        for p in soup.find_all('p'):
            text = p.get_text(strip=True)
            if text and len(text) > 20:
                content_parts.append(text)

    if not content_parts:
        body = soup.find('body')
        if body:
            text = body.get_text(separator=' ', strip=True)
            if text:
                content_parts.append(text[:5000])

    content = ' '.join(content_parts)
    content = re.sub(r'\s+', ' ', content).strip()

    return title, heading, content


def extract_wikipedia_content(soup: BeautifulSoup, url: str) -> Tuple[str, str, str]:
    for tag in soup.find_all(['script', 'style', 'nav', 'footer', 'header', 'aside',
                               'sup', 'table', 'noscript']):
        tag.decompose()

    title = ""
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.get_text(strip=True)
        title = re.sub(r'\s*-\s*Wikipedia$', '', title).strip()

    heading = ""
    h1 = soup.find('h1', id='firstHeading')
    if h1:
        heading = h1.get_text(strip=True)
    if not heading:
        h1 = soup.find('h1')
        if h1:
            heading = h1.get_text(strip=True)

    content_parts = []
    content_div = soup.find('div', id='mw-content-text') or soup.find('div', class_='mw-parser-output')
    if content_div:
        for p in content_div.find_all(['p', 'h2', 'h3', 'h4', 'li'], recursive=True):
            if p.get('id') == 'toc' or p.find_parent('table', id='toc'):
                continue
            text = p.get_text(strip=True)
            if text and len(text) > 30:
                content_parts.append(text)
                if len(content_parts) >= 100:
                    break

    content = ' '.join(content_parts)
    content = re.sub(r'\[\d+\]', '', content)
    content = re.sub(r'\s+', ' ', content).strip()

    if not content:
        body = soup.find('body')
        if body:
            text = body.get_text(separator=' ', strip=True)
            text = re.sub(r'\[\d+\]', '', text)
            content = re.sub(r'\s+', ' ', text).strip()[:5000]

    return title, heading, content


def fetch_page(url: str) -> Optional[BeautifulSoup]:
    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"  [ERROR] Failed to fetch {url}: {e}")
        return None


def crawl() -> List[Dict]:
    documents = []
    total = len(CURATED_URLS)

    print(f"LakbaySearch Crawler")
    print(f"{'=' * 60}")
    print(f"Starting crawl of {total} Philippine tourism URLs...")
    print(f"{'=' * 60}\n")

    for idx, entry in enumerate(CURATED_URLS, start=1):
        url = entry["url"]
        source = entry["source"]
        category = entry["category"]

        print(f"[{idx:02d}/{total:02d}] Crawling: {url}")
        print(f"         Source: {source} | Category: {category}")

        soup = fetch_page(url)
        if soup is None:
            print(f"         [SKIPPED] Could not fetch page.\n")
            continue

        try:
            if source == "en.wikipedia.org":
                title, heading, content = extract_wikipedia_content(soup, url)
            else:
                title, heading, content = extract_dot_content(soup, url)
        except Exception as e:
            print(f"         [ERROR] Extraction failed: {e}")
            print()
            continue

        if not content or len(content) < 50:
            print(f"         [SKIPPED] Insufficient content ({len(content)} chars).\n")
            continue

        doc = {
            "id": idx,
            "title": title if title else heading if heading else url,
            "heading": heading if heading else title if title else "",
            "url": url,
            "content": content,
            "source": source,
            "category": category,
        }
        documents.append(doc)
        print(f"         [OK] Title: {doc['title'][:60]}...")
        print(f"         Content: {len(content)} chars\n")

        time.sleep(CRAWL_DELAY)

    print(f"{'=' * 60}")
    print(f"Crawl complete. {len(documents)} documents collected.")
    print(f"{'=' * 60}")

    return documents


def save_documents(documents: List[Dict]) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DOCUMENTS_PATH, 'w', encoding='utf-8') as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)
    print(f"Documents saved to {DOCUMENTS_PATH}")


def load_documents() -> List[Dict]:
    if not os.path.exists(DOCUMENTS_PATH):
        print(f"Warning: {DOCUMENTS_PATH} not found. Run crawler.py first.")
        return []
    with open(DOCUMENTS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    documents = crawl()
    save_documents(documents)
    print(f"\nDone. {len(documents)} documents saved to data/documents.json.")


if __name__ == "__main__":
    main()