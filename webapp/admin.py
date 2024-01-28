from django.contrib import admin
from django.utils.html import format_html
from .models import Flower, Order, OrderItem, Customer, Review

class FlowerAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity_available', 'category', 'display_image']
    search_fields = ['name']

    def display_image(self, obj):
        return format_html('<img src="{}" style="max-width: 50px; max-height: 50px;" />', obj.image.url)

    display_image.short_description = 'Image'

    fieldsets = [
        ('Product Information', {'fields': ['name', 'description', 'price', 'image', 'quantity_available', 'category']}),
    ]
    
    readonly_fields = ['display_image_preview']

    def display_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 50px; max-height: 50px;" />', obj.image.url)
        else:
            return "No image"

    display_image_preview.short_description = 'Image Preview'

    # Exclude date_added from the form
    exclude = ['date_added']

admin.site.register(Flower, FlowerAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'date_ordered', 'total_price', 'status']
    search_fields = ['id', 'customer__username']
    list_filter = ['status']

admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'flower', 'quantity', 'subtotal']
    search_fields = ['order__id', 'flower__name']

admin.site.register(OrderItem, OrderItemAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'address']
    search_fields = ['user__username']

admin.site.register(Customer, CustomerAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['customer', 'flower', 'rating', 'date_posted']
    search_fields = ['customer__username', 'flower__name']

admin.site.register(Review, ReviewAdmin)

