from django.contrib import admin
from .models import Product, Item, ItemImage
from django.utils.html import format_html

class ItemImageInline(admin.TabularInline):  # or use StackedInline for a different layout
    model = ItemImage
    extra = 1  # Number of empty forms to display
    readonly_fields = ('thumbnail_preview',)
    fields = ('image', 'is_primary', 'thumbnail_preview')
    
    def thumbnail_preview(self, obj):
        if obj.id and obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "No image"
    thumbnail_preview.short_description = 'Preview'

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemImageInline]
    list_display = ('product', 'seller', 'price', 'image_count', 'thumbnail')
    
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

@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin):
    list_display = ('item', 'thumbnail_preview', 'is_primary')
    
    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "No image"
    thumbnail_preview.short_description = 'Preview'


