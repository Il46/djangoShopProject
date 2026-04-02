from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["full_name", "phone", "address"]
        labels = {
            "full_name": "ФИО",
            "phone": "Телефон",
            "address": "Адрес",
        }
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
        }
