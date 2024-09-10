import re
from playwright.sync_api import Playwright, sync_playwright, expect
import requests
from bs4 import BeautifulSoup
def ccScrape(browser, merchant):
    url = f"https://api.instore.bambora.com/api/merchants/{merchant}?embed=aggregations&embed=hostconfiguration&embed=services&embed=history&embed=licensesummary"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Authorization': f"Bearer {BEARER_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        data = response.json()
        return data

    else:
        browser.close()
  
