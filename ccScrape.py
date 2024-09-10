import re
from playwright.sync_api import Playwright, sync_playwright, expect
import requests
from bs4 import BeautifulSoup
def ccScrape(browser, merchant):
    url = f"https://api.instore.bambora.com/api/merchants/{merchant}?embed=aggregations&embed=hostconfiguration&embed=services&embed=history&embed=licensesummary"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6ImNjLWxvZ2lzdGljcyIsIlVzZXIiOiJoYW5uZXMubmlsc3NvbnRlbmduYXNAd29ybGRsaW5lLmNvbSIsIkFjY291bnRJZCI6MTY5LCJBY2NvdW50IjoiY2MtbG9naXN0aWNzIiwibmJmIjoxNzIwNjA4MTg5LCJleHAiOjE3MjA2NDQxODksImlhdCI6MTcyMDYwODE4OSwiaXNzIjoiSW5zdG9yZUFQSSIsImF1ZCI6Ikluc3RvcmVBdWRpZW5jZSJ9.ot5JpC-Ivph8CUu7SmpJGDN4fqqjM_WxRNIa6ytVG34_GOYJiLNTpeSy1a8qaBmYTFhq306kUGPxIDL_UGzvVQJLNY6s8l8liRNUkRS4aerebIcweIL0EYcdljkFbor8ST-JglJ5mEWm-7_HmZT_sa1t1v4gSnw9vuvqW_uq4KZY5ZX49UJOGFbb_Gx2UOlL6v8IP3M3zEhgvGGOqqXmt4zUpxl4B8VsfXcaXLP7W2MXm0tzI1YsYDZTh9BqZ3TcoG3LpV-H9ym2kkgHHa4lsl4uoOvT11Oy3F4XJnzRWZU9ap4s-pDzshYx3CwxGigxW1V1UB-607UuomiucGKhzg"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        data = response.json()
        return data

    else:
        browser.close()
  
