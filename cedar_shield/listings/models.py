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
    
    # Review fields
    review_rating = models.IntegerField(blank=True, null=True, choices=[
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars')
    ])
    review_comments = models.TextField(blank=True, null=True)
    review_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.status == 'sold' and not self.sale_date:
            from django.utils import timezone
            self.sale_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        #return f"{self.item.name} listing"
        return f"{self.item.product.name} by {self.item.seller.username} listing"


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listing_images/')
    is_primary = models.BooleanField(default=False)
    caption = models.CharField(max_length=255, blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # If this is the first image for the listing, make it primary
        if not self.listing.images.exists():
            self.is_primary = True
        # If this image is being set as primary, unset any existing primary
        elif self.is_primary:
            self.listing.images.filter(is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image {self.id} for listing {self.listing.id}"


