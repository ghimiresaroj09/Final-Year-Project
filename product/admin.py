from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
import csv, io
from django.urls import reverse

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


@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    search_fields = ('title', 'keywords', 'content')
    list_filter = ('is_active',)
    ordering = ('-created_at',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-kb/', self.admin_site.admin_view(self.import_kb), name='product_knowledgebase_import'),
        ]
        return custom_urls + urls

    def import_kb(self, request):
        if request.method == 'POST' and request.FILES.get('csv_file'):
            csv_file = request.FILES['csv_file']
            try:
                data = csv_file.read().decode('utf-8')
            except Exception:
                messages.error(request, 'Unable to read uploaded file. Ensure it is UTF-8 encoded.')
                return redirect(reverse('admin:product_knowledgebase_changelist'))

            reader = csv.DictReader(io.StringIO(data))
            created = 0
            updated = 0
            for i, row in enumerate(reader, start=1):
                title = (row.get('title') or '').strip()
                content = (row.get('content') or '').strip()
                keywords = (row.get('keywords') or '').strip()
                is_active_raw = (row.get('is_active') or '1').strip()
                is_active = str(is_active_raw).lower() in ('1', 'true', 'yes', 'y')

                if not title or not content:
                    messages.warning(request, f"Skipping row {i}: missing title or content")
                    continue

                obj, created_flag = KnowledgeBase.objects.update_or_create(
                    title=title,
                    defaults={
                        'content': content,
                        'keywords': keywords,
                        'is_active': is_active,
                    }
                )
                if created_flag:
                    created += 1
                else:
                    updated += 1

            messages.success(request, f'Import finished: created={created}, updated={updated}')
            return redirect(reverse('admin:product_knowledgebase_changelist'))

        context = dict(self.admin_site.each_context(request))
        return render(request, 'admin/import_kb.html', context)