from django.contrib import admin
from .models import Category, BlogPost, BlogComment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'status', 'featured', 'published_at', 'views')
    list_filter = ('status', 'category', 'featured', 'published_at')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    readonly_fields = ('views', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'category', 'excerpt', 'content', 'featured_image')
        }),
        ('Metadata', {
            'fields': ('author', 'status', 'featured', 'published_at')
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'post', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('author_name', 'content', 'post__title')
    readonly_fields = ('created_at',)
