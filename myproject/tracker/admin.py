from django.contrib import admin
from .models import Asset, PriceRecord


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'tunnel_input_type', 'upper_tunnel', 'lower_tunnel',
        'last_price', 'tracking_frequency', 'notify_only_once', 'email'
    )
    list_filter = ('tunnel_input_type', 'notify_only_once')
    search_fields = ('name', 'email')
    ordering = ('name',)
    readonly_fields = ('last_price',)


@admin.register(PriceRecord)
class PriceRecordAdmin(admin.ModelAdmin):
    list_display = ('asset', 'price', 'scraped_at')
    list_filter = ('asset',)
    search_fields = ('asset__name',)
    ordering = ('-scraped_at',)
