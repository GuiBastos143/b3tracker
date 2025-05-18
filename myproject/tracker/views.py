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
            asset = form.save()
            return redirect('asset_detail', pk=asset.pk)
    else:
        form = AssetForm()
    return render(request, 'tracker/asset_form.html', {'form': form})

def asset_detail(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    prices = asset.price_records.order_by('scraped_at')
    return render(request, 'tracker/asset_detail.html', {
        'asset': asset,
        'prices': prices
    })