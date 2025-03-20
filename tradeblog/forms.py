# tradeblog/forms.py
from django import forms
from .models import TradePost

class TradePostForm(forms.ModelForm):
    class Meta:
        model = TradePost
        fields = ['title', 'content', 'chart_image']