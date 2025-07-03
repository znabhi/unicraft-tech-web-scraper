import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re

def extract_info(url):
    def parse_page(soup, base_url):
        text = soup.get_text(separator=' ')
        # company name
        title = soup.title.string.strip() if soup.title else urlparse(base_url).netloc
        h1 = soup.find('h1')
        name = h1.get_text(strip=True) if h1 else title
        # emails
        raw = re.findall(r"[\w\.-]+@[\w\.-]+\.[\w\.-]+", text)
        mailto = [a['href'][7:] for a in soup.find_all('a', href=True) if a['href'].startswith('mailto:')]
        inline = [a.get_text(strip=True) for a in soup.find_all('a') if '@' in a.get_text()]
        emails = set(raw + mailto + inline)
        # phones (Indian)
        rawp = re.findall(r"(?:\+91[\s-]?)?[6-9]\d{9}", text)
        tel = [a['href'][4:] for a in soup.find_all('a', href=True) if a['href'].startswith('tel:')]
        inlinep = [a.get_text(strip=True) for a in soup.find_all('a') if re.match(r"(?:\+91[\s-]?)?[6-9]\d{9}", a.get_text(strip=True))]
        phones = set(rawp + tel + inlinep)
        return name, emails, phones

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        name, emails, phones = parse_page(soup, url)
        # if nothing found, look for contact page links
        if not emails and not phones:
            for a in soup.find_all('a', href=True):
                if any(k in a.get_text(strip=True).lower() for k in ['contact','support','help']):
                    contact_url = urljoin(url, a['href'])
                    resp2 = requests.get(contact_url, headers=headers, timeout=10)
                    soup2 = BeautifulSoup(resp2.text, 'html.parser')
                    name2, emails2, phones2 = parse_page(soup2, contact_url)
                    emails |= emails2
                    phones |= phones2
                    break
        return {'company_name': name, 'emails': list(emails), 'phones': list(phones), 'website': url}
    except Exception as e:
        return {'company_name': 'Unknown', 'emails': [], 'phones': [], 'website': url, 'error': str(e)}
