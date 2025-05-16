from django.db import models

class Asset(models.Model):
    TUNNEL_CHOICES = [
        ('static', 'Static'),
        ('dynamic_sync', 'Dynamic Synchronous'),
        ('dynamic_async', 'Dynamic Unsynchronous'),
    ]
    OPTION_TYPE_CHOICES = [
    ('call', 'Call'),
    ('put', 'Put'),
    ]
    name = models.CharField(max_length=100)
    tunnel_type = models.CharField(max_length=20, choices=TUNNEL_CHOICES)
    volatility = models.FloatField()
    strike_price = models.FloatField()
    expiration_days = models.IntegerField()
    interest_rate = models.FloatField(default=0.13)
    email = models.EmailField()
    last_price = models.FloatField(null=True, blank=True)
    notified = models.BooleanField(default=False)
    notify_only_once = models.BooleanField(default=False)
    tracking_frequency = models.IntegerField(default=5, help_text="Frequency to check the asset (minutes)")
    lower_tunnel = models.FloatField(null=True, blank=True)
    upper_tunnel = models.FloatField(null=True, blank=True)
    option_type = models.CharField(max_length=4, choices=OPTION_TYPE_CHOICES)

    def __str__(self):
        return self.name

class PriceRecord(models.Model):
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE, related_name='price_records')
    price = models.FloatField()
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asset.name} - {self.price} @ {self.scraped_at}"
