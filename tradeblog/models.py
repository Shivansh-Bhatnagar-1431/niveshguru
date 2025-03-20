from django.db import models

# Create your models here.
# tradeblog/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TradePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    chart_image = models.ImageField(upload_to='trade_charts/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title