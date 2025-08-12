from django.contrib import admin
from .models import Customer, Order, OrderItem

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone_number')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('total_price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_price', 'created_at', 'payment_method')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('customer__name', 'customer__email')
    readonly_fields = ('created_at', 'total_price')
    ordering = ('-created_at',)
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('customer', 'status', 'created_at')
        }),
        ('Delivery Details', {
            'fields': ('delivery_address', 'special_instructions')
        }),
        ('Payment', {
            'fields': ('payment_method',)
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity', 'total_price')
    list_filter = ('menu_item',)
    search_fields = ('order__customer__name', 'menu_item__name')
    readonly_fields = ('total_price',)
