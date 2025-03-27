from django.contrib import admin
from django.utils.html import format_html
from .models import Listing, ListingImage

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1
    readonly_fields = ('thumbnail_preview', 'upload_date')
    fields = ('image', 'is_primary', 'caption', 'thumbnail_preview', 'upload_date')
    
    def thumbnail_preview(self, obj):
        if obj.id and obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "No image"
    thumbnail_preview.short_description = 'Preview'

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('item', 'listed_price', 'status', 'sale_type', 'listed_date', 'thumbnail')
    list_filter = ('status', 'sale_type', 'listed_date')
    search_fields = ('item__product__name', 'item__seller__username')
    readonly_fields = ('listed_date',)
    inlines = [ListingImageInline]
    
    def thumbnail(self, obj):
        # Get the primary image or the first image
        image = obj.images.filter(is_primary=True).first() or obj.images.first()
        if image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', image.image.url)
        return "-"
    thumbnail.short_description = 'Thumbnail'

@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ('listing', 'thumbnail_preview', 'is_primary', 'caption', 'upload_date')
    list_filter = ('listing', 'is_primary', 'upload_date')
    search_fields = ('listing__item__product__name', 'caption')
    readonly_fields = ('upload_date', 'thumbnail_preview')
    
    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "No image"
    thumbnail_preview.short_description = 'Preview'

