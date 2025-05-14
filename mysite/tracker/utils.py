import requests
from bs4 import BeautifulSoup
from django.core.mail import send_mail
from django.conf import settings

def fetch_asset_price(asset_name):
    response = requests.get('&&url&&')
    soup = BeautifulSoup(response.content, 'html.parser')
    price_element = soup.find('span', {'id': f'price_{asset_name}'})
    if price_element:
        price_text = price_element.text.strip().replace(',', '.')
        try:
            return float(price_text)
        except ValueError:
            return None
    return None

def send_price_alert_sell(asset_name, price, email):
    subject = f'Price Alert for {asset_name}'
    message = f'The price of {asset_name} has reached {price}. It is time to sell!'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

def send_price_alert_buy(asset_name, price, email):
    subject = f'Price Alert for {asset_name}'
    message = f'The price of {asset_name} has reached {price}. It is time to buy!'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])