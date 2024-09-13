from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # How many empty rows to display by default

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display= ['id','user','email','full_name','total_amount','shipping_address','date_ordered','shipping_status','date_shipped']
    list_display_links = ['id','user','email']
    list_filter = ['shipping_status']
    search_fields = ['user__username']
    list_per_page=10

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)

