from django.core.management.base import BaseCommand
from tracker.models import Asset
from tracker.utils import fetch_asset_price, send_price_alert_sell, send_price_alert_buy
from tracker.tunnel import calculate_tunnel_bounds
from tracker.models import Asset, PriceRecord

...

for asset in Asset.objects.all():
    price = fetch_asset_price(asset.url, asset.name)
    if price:
        asset.last_price = price
        PriceRecord.objects.create(asset=asset, price=price)
        t = asset.expiration_days / 252  # Assuming 252 trading days in a year
        low, high = calculate_tunnel_bounds(
            price, asset.strike_price, t, asset.interest_rate, asset.volatility, method=asset.tunnel_type
        )
        if price < low:
            if not asset.notified:
                send_price_alert_buy(asset.name, price, asset.email)
                asset.notified = True
        elif price > high:
            if not asset.notified:
                send_price_alert_sell(asset.name, price, asset.email)
                asset.notified = True
        else:
            asset.notified = False
        asset.save()