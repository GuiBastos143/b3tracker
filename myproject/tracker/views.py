from django.shortcuts import render, get_object_or_404, redirect
from .models import Asset, PriceRecord
from .forms import AssetForm
from .utils import fetch_asset_price
from .tunnel import tunnel_limits

def asset_list(request):
    assets = Asset.objects.all()
    return render(request, 'tracker/asset_list.html', {'assets': assets})

def asset_create(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            # Scrape price as soon as asset is created
            price = fetch_asset_price(asset.name)
            if price is not None:
                asset.last_price = price
            # Calculate tunnels using the user's params
            S = asset.last_price if asset.last_price else asset.strike_price  # fallback if no price
            K = asset.strike_price
            r = asset.interest_rate
            sigma = asset.volatility
            t = asset.expiration_days / 252
            option_type = asset.option_type
            tunnel_type = asset.tunnel_type

            lower, upper = tunnel_limits(S, K, r, sigma, t, tunnel_type, option_type)
            asset.lower_tunnel = lower
            asset.upper_tunnel = upper

            asset.save()
            PriceRecord.objects.create(asset=asset, price=price)
            return redirect('asset_detail', pk=asset.pk)
    else:
        form = AssetForm()
    return render(request, 'tracker/asset_form.html', {'form': form})

def asset_detail(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    prices = asset.price_records.order_by('scraped_at') 
    first_price = prices.first()
    latest_price = prices.last()
    return render(request, 'tracker/asset_detail.html', {
        'asset': asset,
        'prices': prices,
        'first_price': first_price,
        'latest_price': latest_price
    })