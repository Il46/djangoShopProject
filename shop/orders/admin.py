from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ["product", "quantity", "price"]
    readonly_fields = ["price"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "full_name", "phone", "status", "created_at"]
    list_filter = ["status", "created_at", "user"]
    search_fields = ["full_name", "phone", "address", "user__username", "user__email"]
    inlines = [OrderItemInline]
    fieldsets = (
        ("Customer Information", {
            "fields": ("user", "full_name", "phone", "address")
        }),
        ("Order Status", {
            "fields": ("status",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    readonly_fields = ["created_at", "updated_at"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "product", "quantity", "price"]
    list_filter = ["order__created_at", "product__category"]
    search_fields = ["order__full_name", "product__name"]
