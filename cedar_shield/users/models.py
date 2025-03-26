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

    
    # Inventory products - using related_name to access from both directions
#    products_bought = models.ManyToManyField(
#        'inventory.Product',
#        related_name='buyers',
#        blank=True
#    )
#    products_selling = models.ManyToManyField(
#        'inventory.Product',
#        related_name='sellers', 
#        blank=True
#    )

    def __str__(self):
        return f"{self.username} ({self.email})"

    class Meta:
        ordering = ['-date_joined']

