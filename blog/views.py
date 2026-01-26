from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import BlogPost, Category, BlogComment
from .forms import BlogCommentForm
from django.contrib import messages

def blog_list(request):
    """Display all published blog posts with filtering and pagination"""
    posts = BlogPost.objects.filter(status='published').select_related('category')
    
    # Filter by category if provided
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    # Get all categories for filter sidebar
    categories = Category.objects.all()
    
    # Pagination
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get featured posts for sidebar
    featured_posts = BlogPost.objects.filter(
        status='published',
        featured=True
    ).order_by('-published_at')[:3]
    
    context = {
        'page_obj': page_obj,
        'posts': page_obj.object_list,
        'categories': categories,
        'featured_posts': featured_posts,
        'search_query': search_query,
        'selected_category': category_slug,
    }
    
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, slug):
    """Display single blog post with comments"""
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    
    # Increment view count
    post.increment_views()
    
    # Get comments
    comments = post.comments.filter(is_approved=True).order_by('-created_at')
    
    # Get related posts (same category)
    related_posts = BlogPost.objects.filter(
        category=post.category,
        status='published'
    ).exclude(id=post.id).order_by('-published_at')[:3]
    
    # Get featured posts for sidebar
    featured_posts = BlogPost.objects.filter(
        status='published',
        featured=True
    ).exclude(id=post.id).order_by('-published_at')[:3]
    
    # Handle comment submission
    form = None
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f"/user/login/?next={request.path}")
        
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, "Thank you for your comment. It will be displayed once admin verify it.")
            return redirect('blog:blog_detail', slug=post.slug)
        
    else:
        form = BlogCommentForm() if request.user.is_authenticated else None
    
    context = {
        'post': post,
        'comments': comments,
        'related_posts': related_posts,
        'featured_posts': featured_posts,
        'comment_form': form,
    }
    
    return render(request, 'blog/blog_detail.html', context)
