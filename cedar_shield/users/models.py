from django.db import models


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class User(models.Model):
    # Basic user information
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    
    # Rating fields - seller_rating is updated by Listing.update_seller_rating()
    seller_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    seller_review_count = models.PositiveIntegerField(default=0)  # New field
    buyer_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    # Contact information
    phone = models.CharField(max_length=20, blank=True)
    
    # Shipping Address
    shipping_address = models.TextField(blank=True)
    shipping_city = models.CharField(max_length=100, blank=True)
    shipping_state = models.CharField(max_length=100, blank=True)
    shipping_country = models.CharField(max_length=100, blank=True)
    shipping_postal_code = models.CharField(max_length=20, blank=True)

    # Billing Address
    billing_address = models.TextField(blank=True)
    billing_city = models.CharField(max_length=100, blank=True)
    billing_state = models.CharField(max_length=100, blank=True)
    billing_country = models.CharField(max_length=100, blank=True)
    billing_postal_code = models.CharField(max_length=20, blank=True)

    # Payment information
    royalties_payment_method = models.CharField(max_length=20, choices=[
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('crypto', 'Crypto'),
        ('other', 'Other')
    ], blank=True, null=True)  # Added blank/null for flexibility
    royalties_payment_account_id = models.CharField(max_length=100, blank=True)

    # Relationships:
    # - items: Available via related_name from Item model
    # - purchased_listings: Available via related_name from Listing model

    @property
    def listings(self):
        """Get all listings where this user is the seller"""
        from listings.models import Listing
        return Listing.objects.filter(item__seller=self)
    
    @property
    def active_listings(self):
        """Get active listings where this user is the seller"""
        from listings.models import Listing
        return Listing.objects.filter(item__seller=self, status='active')

    def __str__(self):
        return f"{self.username} ({self.email})"

    class Meta:
        ordering = ['-date_joined']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    interests = models.ManyToManyField(Interest, blank=True)
    favorite_brands = models.JSONField(default=list, blank=True)
    favorite_categories = models.JSONField(default=list, blank=True)
    liked_items = models.ManyToManyField('products.Item', related_name='liked_by', blank=True)
    viewed_items = models.ManyToManyField('products.Item', related_name='viewed_by', through='ViewEvent', blank=True)
    saved_searches = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"


class ViewEvent(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    item = models.ForeignKey('products.Item', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_profile', 'item')
        indexes = [
            models.Index(fields=['user_profile', 'item']),
        ]


# marketplace/models.py
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
