from django.contrib import admin
from .models import Product, Item, ProductImage
from django.utils.html import format_html

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('thumbnail_preview',)
    fields = ('image', 'is_primary', 'thumbnail_preview')
    
    def thumbnail_preview(self, obj):
        if obj.id and obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "No image"
    thumbnail_preview.short_description = 'Preview'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('sku', 'name', 'brand', 'category', 'image_count', 'thumbnail')
    list_filter = ('brand', 'category')
    search_fields = ('sku', 'name', 'model')
    
    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = 'Images'
    
    def thumbnail(self, obj):
        # Get the primary image or the first image
        image = obj.images.filter(is_primary=True).first() or obj.images.first()
        if image:
            return format_html('<img src="{}" width="50" height="50" />', image.image.url)
        return "-"
    thumbnail.short_description = 'Thumbnail'

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'product', 'seller', 'price', 'is_approved')
    list_filter = ('is_approved', 'seller')
    search_fields = ('uuid', 'product__name', 'product__sku')
    # Removed the ProductImageInline because it's now related to Product, not Item

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'thumbnail_preview', 'is_primary')
    list_filter = ('product', 'is_primary')
    
    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "No image"
    thumbnail_preview.short_description = 'Preview'