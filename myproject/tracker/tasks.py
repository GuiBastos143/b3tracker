from celery import shared_task
from django.utils import timezone
from .models import Asset, PriceRecord
from .utils import fetch_asset_price, send_price_alert_buy, send_price_alert_sell 

@shared_task
def update_asset_prices():
    now = timezone.now()
    for asset in Asset.objects.all():
        last_record = asset.price_records.order_by('-scraped_at').first()
        due = (
            not last_record or
            (now - last_record.scraped_at).total_seconds() >= asset.tracking_frequency * 60
        )
        if due:
            price = fetch_asset_price(asset.name)
            if price is not None:
                asset.last_price = price
                asset.save()
                PriceRecord.objects.create(asset=asset, price=price)
                
                if asset.lower_tunnel is not None and price < asset.lower_tunnel:
                    send_price_alert_buy(asset.name, price, asset.email)
                elif asset.upper_tunnel is not None and price > asset.upper_tunnel:
                    send_price_alert_sell(asset.name, price, asset.email)