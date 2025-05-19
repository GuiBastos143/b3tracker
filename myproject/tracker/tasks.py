from celery import shared_task
from django.utils import timezone
from .models import Asset, PriceRecord
from .utils import fetch_asset_price, send_price_alert_buy
from .utils import send_price_alert_sell


@shared_task
def update_asset_prices():
    """
    Periodic Celery task to update asset prices.

    - Iterates through all configured assets.
    - Checks if it's time to fetch a new price based on the tracking frequency.
    - Fetches the latest price and stores it.
    - Checks price against tunnel thresholds and sends alerts if needed.
    """
    now = timezone.now()
    for asset in Asset.objects.all():
        last_record = asset.price_records.order_by('-scraped_at').first()
        due = (
            not last_record or
            (now - last_record.scraped_at).total_seconds()
            >= asset.tracking_frequency * 60
        )
        if due:
            price = fetch_asset_price(asset.name)
            if price is not None:
                asset.last_price = price
                asset.save()
                PriceRecord.objects.create(asset=asset, price=price)
                if price < asset.lower_tunnel:
                    if not asset.notified or not asset.notify_only_once:
                        send_price_alert_buy(asset.name, price, asset.email)
                        if asset.notify_only_once:
                            asset.notified = True
                            asset.save()
                elif price > asset.upper_tunnel:
                    if not asset.notified or not asset.notify_only_once:
                        send_price_alert_sell(asset.name, price, asset.email)
                        if asset.notify_only_once:
                            asset.notified = True
                            asset.save()
                else:
                    if asset.notified:
                        asset.notified = False
                        asset.save()
