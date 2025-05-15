import requests
from bs4 import BeautifulSoup
from django.core.mail import send_mail
from django.conf import settings

def fetch_google_price(ticker):
    url = f"https://www.google.com/finance/quote/{ticker}:BVMF"
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers, timeout=10)
    if r.status_code != 200:
        return None
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        # Google's price is usually in this class (as of May 2025)
        price_span = soup.find('div', class_="YMlKec fxKbKc")
        if price_span:
            price = float(price_span.text.replace('R$', '').replace(',', '').strip())
            return price
    except Exception:
        return None
    return None

def fetch_yahoo_price(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}.SA'
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers, timeout=10)
    if r.status_code != 200:
        return None
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        price_tag = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'})
        if price_tag:
            return float(price_tag.text.replace(',', ''))
    except Exception:
        return None
    return None

def fetch_asset_price(ticker):
    # First try to fetch from Google
    # Google Finance URL format: https://www.google.com/finance/quote/{ticker}:BVMF
    price = fetch_google_price(ticker)
    if price is not None:
        print(f"Fetched from Google: {price}")
        return price
    # If Google fails, try Yahoo
    # Yahoo Finance URL format: https://finance.yahoo.com/quote/{ticker}.SA
    price = fetch_yahoo_price(ticker)
    if price is not None:
        print(f"Fetched from Yahoo: {price}")
        return price
    print("Failed to fetch price from both sources.")
    return None

def send_price_alert_sell(asset_name, price, email):
    subject = f'Price Alert for {asset_name}'
    message = f'The price of {asset_name} has reached {price}. It is time to sell!'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

def send_price_alert_buy(asset_name, price, email):
    subject = f'Price Alert for {asset_name}'
    message = f'The price of {asset_name} has reached {price}. It is time to buy!'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])