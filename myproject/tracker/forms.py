from django import forms
from .models import Asset

class AssetForm(forms.ModelForm):

    TUNNEL_INPUT_CHOICES = [
        ('manual', 'Manual fixed input'),
        ('percentage', 'Percentage over first price'),
    ]

    tunnel_input_type = forms.ChoiceField(
        choices=TUNNEL_INPUT_CHOICES,
        widget=forms.RadioSelect,
        initial='manual',
        label="Tunnel input type"
    )

    class Meta:
        model = Asset
        fields = [
            'name', 'upper_tunnel', 'lower_tunnel', 'tunnel_input_type',
            'tracking_frequency', 'notify_only_once', 'email'
        ]
        widgets = {
            'upper_tunnel': forms.NumberInput(attrs={'step': 0.01}),
            'lower_tunnel': forms.NumberInput(attrs={'step': 0.01}),
            'tracking_frequency': forms.NumberInput(attrs={
                'type': 'range', 'min': 1, 'max': 1440, 'step': 1, 'value': 5,
                'oninput': "document.getElementById('freq_output').value=this.value"
            }),
            'notify_only_once': forms.CheckboxInput(),
            'email': forms.EmailInput(),
        }