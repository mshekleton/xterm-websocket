from django.db import models

class SocialMediaEvent(models.Model):
    event_id = models.AutoField(primary_key=True)
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

    def __str__(self):
        return f"{self.platform} event: {self.link}"
