from django.db import models
from users.models import User
from products.models import Item, Product

class Listing(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    listed_price = models.DecimalField(max_digits=10, decimal_places=2)
    listed_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
        ('sold', 'Sold')
    ])
    sale_type = models.CharField(max_length=20, choices=[
        ('auction', 'Auction'),
        ('offer', 'Offer')
    ], default='offer')

    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sale_date = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.status == 'sold' and not self.sale_date:
            from django.utils import timezone
            self.sale_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        #return f"{self.item.name} listing"
        return f"{self.item.product.name} by {self.item.seller.username} listing"



