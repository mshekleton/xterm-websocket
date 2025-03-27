from django.db import models

# Create your models here.
class User(models.Model):
    # Basic user information
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    seller_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
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
    ])
    royalties_payment_account_id = models.CharField(max_length=100, blank=True)

    # User's listings and items
    #listings = models.ManyToManyField('marketplace.Listing', related_name='sellers', blank=True)
    #purchased_items = models.ManyToManyField('marketplace.Item', related_name='buyers', blank=True)


    def __str__(self):
        return f"{self.username} ({self.email})"

    class Meta:
        ordering = ['-date_joined']

