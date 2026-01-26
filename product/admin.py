from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','image_tag','price', 'category', 'is_sale','sale_price','on_stock','out_of_stock')
    list_display_links = ('id','name','image_tag')
    search_fields = ('name', 'description')
    list_per_page=10
    list_filter=('category','is_sale','out_of_stock')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

# Homepage Models Admin
@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')
    ordering = ('order', '-created_at')

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'updated_at')
    list_filter = ('is_active',)

@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('stat_type', 'value', 'label', 'is_active', 'order')
    list_filter = ('is_active', 'stat_type')
    ordering = ('order',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'rating', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'rating')
    search_fields = ('name', 'content')
    ordering = ('order', '-created_at')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'is_active', 'order', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'position', 'bio')
    ordering = ('order', 'name')

@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'email', 'is_active', 'updated_at')
    list_filter = ('is_active',)