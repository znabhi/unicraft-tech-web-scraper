from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re, time

def extract_dynamic_info(url):
    try:
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.TAG_NAME,'body')))
        time.sleep(2)
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);'); time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        # parse same as static
        def parse(soup, base):
            txt=soup.get_text(separator=' ')
            title=soup.title.string.strip() if soup.title else urlparse(base).netloc
            h1=soup.find('h1'); name=h1.get_text(strip=True) if h1 else title
            raw=re.findall(r"[\w\.-]+@[\w\.-]+\.[\w\.-]+",txt)
            mailto=[a['href'][7:] for a in soup.find_all('a',href=True) if a['href'].startswith('mailto:')]
            inline=[a.get_text(strip=True) for a in soup.find_all('a') if '@' in a.get_text()]
            emails=set(raw+mailto+inline)
            rawp=re.findall(r"(?:\+91[\s-]?)?[6-9]\d{9}",txt)
            tel=[a['href'][4:] for a in soup.find_all('a',href=True) if a['href'].startswith('tel:')]
            inlinep=[a.get_text(strip=True) for a in soup.find_all('a') if re.match(r"(?:\+91[\s-]?)?[6-9]\d{9}",a.get_text(strip=True))]
            phones=set(rawp+tel+inlinep)
            return name,emails,phones
        name,emails,phones = parse(soup,url)
        # if none, follow contact/support/help
        if not emails and not phones:
            for a in soup.find_all('a',href=True):
                txt=a.get_text(strip=True).lower()
                if any(k in txt for k in ['contact','support','help']):
                    next_url=urljoin(url,a['href'])
                    driver.get(next_url); time.sleep(2)
                    soup2=BeautifulSoup(driver.page_source,'html.parser')
                    n2,e2,p2=parse(soup2,next_url)
                    emails|=e2; phones|=p2
                    break
        driver.quit()
        return {'company_name': name, 'emails':list(emails), 'phones':list(phones), 'website':url}
    except Exception as e:
        return {'company_name':'Unknown','emails':[],'phones':[],'website':url,'error':str(e)}
