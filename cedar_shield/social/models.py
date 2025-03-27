from django.db import models
from products.models import Item

class SocialMediaEvent(models.Model):
    event_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, related_name='social_events', on_delete=models.CASCADE)
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'), 
        ('tiktok', 'TikTok'),
        ('x', 'X/Twitter'),
        ('snapchat', 'Snapchat'),
        ('youtube', 'YouTube'),
        ('pinterest', 'Pinterest'),
        ('linkedin', 'LinkedIn'),
        ('other', 'Other')
    ]
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    link = models.URLField()
    event_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.platform} event for {self.item}: {self.link}"
