from django.contrib import admin
from .models import User, UserProfile, Interest, ViewEvent, Category, Brand

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 
                   'seller_rating', 'seller_review_count', 'date_joined')
    list_filter = ('is_active', 'is_verified', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_verified')
        }),
        ('Ratings', {
            'fields': ('seller_rating', 'seller_review_count', 'buyer_rating')
        }),
        ('Contact', {
            'fields': ('phone',)
        }),
        ('Shipping Address', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_state', 
                      'shipping_country', 'shipping_postal_code')
        }),
        ('Billing Address', {
            'fields': ('billing_address', 'billing_city', 'billing_state', 
                      'billing_country', 'billing_postal_code')
        }),
        ('Payment Information', {
            'fields': ('royalties_payment_method', 'royalties_payment_account_id')
        })
    )
    readonly_fields = ('date_joined',)

class ViewEventInline(admin.TabularInline):
    model = ViewEvent
    extra = 0
    readonly_fields = ('viewed_at',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_interests', 'get_favorite_brands')
    search_fields = ('user__username', 'user__email', 'bio')
    filter_horizontal = ('interests', 'liked_items')
    inlines = [ViewEventInline]
    
    def get_interests(self, obj):
        return ", ".join([i.name for i in obj.interests.all()[:5]])
    get_interests.short_description = 'Interests'
    
    def get_favorite_brands(self, obj):
        if isinstance(obj.favorite_brands, list):
            return ", ".join(obj.favorite_brands[:5])
        return str(obj.favorite_brands)[:50]
    get_favorite_brands.short_description = 'Favorite Brands'
    
    def get_viewed_items(self, obj):
        return ", ".join([str(i.product) for i in obj.viewed_items.all()[:5]])
    get_viewed_items.short_description = 'Recently Viewed'

@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ViewEvent)
class ViewEventAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'item', 'viewed_at')
    list_filter = ('viewed_at',)
    search_fields = ('user_profile__user__username', 'item__product__name')
    readonly_fields = ('viewed_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)