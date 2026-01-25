from .models import Category, BlogPost

def blog_context(request):
    """Add blog categories and featured posts to template context"""
    return {
        'blog_categories': Category.objects.all(),
        'featured_blog_posts': BlogPost.objects.filter(
            status='published',
            featured=True
        ).order_by('-published_at')[:3],
    }
