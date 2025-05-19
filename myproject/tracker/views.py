from django.shortcuts import render, get_object_or_404, redirect
from .models import Asset, PriceRecord
from .forms import AssetForm

def asset_list(request):
    assets = Asset.objects.all()
    return render(request, 'tracker/asset_list.html', {'assets': assets})

def asset_create(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asset_list')
    else:
        form = AssetForm()
    return render(request, 'tracker/asset_form.html', {'form': form})

def asset_edit(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('asset_detail', pk=asset.pk)
    else:
        form = AssetForm(instance=asset)
    return render(request, 'tracker/asset_form.html', {'form': form, 'editing': True, 'asset': asset})

def asset_delete(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if request.method == 'POST':
        asset.delete()
        return redirect('asset_list')
    return render(request, 'tracker/asset_confirm_delete.html', {'asset': asset})

def asset_detail(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    prices = PriceRecord.objects.filter(asset=asset).order_by('-scraped_at')
    first_price = prices.first().price if prices.exists() else None
    last_price = prices.last().price if prices.exists() else None
    effective_upper = None
    effective_lower = None

    if first_price is not None:
        if asset.tunnel_input_type == 'percentage':
            # upper_tunnel and lower_tunnel are coefficients
            effective_upper = first_price * asset.upper_tunnel
            effective_lower = first_price * asset.lower_tunnel
        else:
            effective_upper = asset.upper_tunnel
            effective_lower = asset.lower_tunnel

    return render(request, 'tracker/asset_detail.html', {
    'asset': asset,
    'effective_upper': effective_upper,
    'effective_lower': effective_lower,
    'prices': prices.order_by('-scraped_at'),
    'first_price': first_price,
    'last_price': last_price,
    })