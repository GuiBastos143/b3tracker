from django.db import models

class Asset(models.Model):
    name = models.CharField(max_length=100)
    lower_tunnel = models.FloatField(default=0)
    upper_tunnel = models.FloatField(default=0)
    tracking_frequency = models.IntegerField(default=5, help_text="Check frequency (minutes)")
    email = models.EmailField()
    notify_only_once = models.BooleanField(default=False)
    notified = models.BooleanField(default=False)
    last_price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class PriceRecord(models.Model):
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE, related_name='price_records')
    price = models.FloatField()
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asset.name} - {self.price} @ {self.scraped_at}"