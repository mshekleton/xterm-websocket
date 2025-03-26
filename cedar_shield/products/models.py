from django.db import models
from brands.models import Brand
from users.models import User

class Product(models.Model):
    sku = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    CATEGORY_CHOICES = [
        ('watches', 'Watches & Timepieces'),
        ('jewelry', 'Fine Jewelry'),
        ('handbags', 'Designer Handbags'),
        ('accessories', 'Luxury Accessories'),
        ('clothing', 'Designer Clothing'),
        ('shoes', 'Designer Shoes'),
        ('sunglasses', 'Designer Sunglasses'),
        ('fragrances', 'Premium Fragrances'),
        ('leather_goods', 'Leather Goods'),
        ('home_decor', 'Luxury Home Decor'),
        ('art', 'Fine Art & Collectibles'),
        ('wine_spirits', 'Fine Wine & Spirits'),
        ('other', 'Other'),
    ]
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    model = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    season = models.CharField(max_length=50, blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    SHIPPING_BOX_CHOICES = [
        ('00', 'Customer Packaging'),
        ('01', 'UPS Letter'),
        ('02', 'UPS Package/Tube'),
        ('03', 'UPS Express Box'),
        ('21', 'UPS Express Box - Small'),
        ('24', 'UPS Express Box - Medium'), 
        ('25', 'UPS Express Box - Large'),
        ('30', 'FedEx Envelope'),
        ('31', 'FedEx Pak'),
        ('32', 'FedEx Box - Small'),
        ('33', 'FedEx Box - Medium'),
        ('34', 'FedEx Box - Large'),
    ]
    shipping_box_class = models.CharField(
        max_length=2,
        choices=SHIPPING_BOX_CHOICES,
        default='00',
        help_text='Shipping package type for carrier APIs'
    )

    def __str__(self):
        return f"{self.name} ({self.sku})"

class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=False) #Admin approval for listing

    def __str__(self):
        return f"{self.product} by {self.seller.username}"

class ItemImage(models.Model):
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_images/')
    is_primary = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        # If this is the first image for the item, make it primary
        if not self.item.images.exists():
            self.is_primary = True
        # If this image is being set as primary, unset any existing primary
        elif self.is_primary:
            self.item.images.filter(is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image {self.id} for {self.item}"
