from django.db import models
from users.models import User
from products.models import Item, Product
from django.db.models import Avg, Count

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

    # Add buyer field with related_name 'purchased_listings'
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                              related_name='purchased_listings')

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
        # Set sale_date when status changes to sold
        if self.status == 'sold' and not self.sale_date:
            from django.utils import timezone
            self.sale_date = timezone.now()
        
        super().save(*args, **kwargs)
        
        # Update seller rating after save if there's a review
        if self.review_rating and self.item and self.item.seller:
            self.update_seller_rating()
    
    def update_seller_rating(self):
        """Update the seller's rating based on all their listing reviews"""
        seller = self.item.seller
        
        # Get all listings for this seller's items that have reviews
        seller_item_ids = seller.items.values_list('id', flat=True)
        reviews = Listing.objects.filter(
            item_id__in=seller_item_ids,
            review_rating__isnull=False
        )
        
        # Calculate average rating and count
        rating_data = reviews.aggregate(
            avg_rating=Avg('review_rating'),
            review_count=Count('id')
        )
        
        # Update seller fields
        if rating_data['avg_rating'] is not None:
            seller.seller_rating = rating_data['avg_rating']
            seller.seller_review_count = rating_data['review_count']
            seller.save(update_fields=['seller_rating', 'seller_review_count'])

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


