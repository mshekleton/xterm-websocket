from django.db import models
from users.models import User
from brands.models import Brand
from listings.models import Listing


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.PROTECT)
    payout_to = models.CharField(max_length=20, choices=[
        ('seller', 'Seller'),
        ('brand', 'Brand'),
        ('platform', 'Platform')
    ])
    transaction_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ])
