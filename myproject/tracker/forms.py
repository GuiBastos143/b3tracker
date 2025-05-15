from django import forms
from .models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = [
            'name', 'asset_type', 'tunnel_type',
            'volatility', 'strike_price', 'expiration_days',
            'interest_rate','notify_only_once', 'tracking_frequency', 'email'
        ]
        widgets = {
            'volatility': forms.NumberInput(attrs={
                'type': 'range', 'min': 0, 'max': 2, 'step': 0.01, 'value': 0.2,
                'oninput': "document.getElementById('vol_output').innerHTML=this.value"
            }),
            'strike_price': forms.NumberInput(attrs={
                'type': 'range', 'min': 0, 'max': 1000, 'step': 1, 'value': 100,
                'oninput': "document.getElementById('strike_output').innerHTML=this.value"
            }),
            'expiration_days': forms.NumberInput(attrs={
                'type': 'range', 'min': 1, 'max': 365, 'step': 1, 'value': 30,
                'oninput': "document.getElementById('exp_output').innerHTML=this.value"
            }),
            'interest_rate': forms.NumberInput(attrs={
                'type': 'range', 'min': 0, 'max': 1, 'step': 0.001, 'value': 0.13,
                'oninput': "document.getElementById('int_output').innerHTML=this.value"
            }),
            'tracking_frequency': forms.NumberInput(attrs={
                'type': 'range', 'min': 1, 'max': 1440, 'step': 1, 'value': 5,
                'oninput': "document.getElementById('freq_output').innerHTML=this.value"
            }),
            'notify_only_once': forms.CheckboxInput(),
        }