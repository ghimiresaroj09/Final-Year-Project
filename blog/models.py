from django.db import models
from django.utils.text import slugify
from django.utils import timezone

class Category(models.Model):
    """Blog Category Model"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='bi bi-file-text', help_text='Bootstrap Icon class')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """Blog Post Model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    author = models.CharField(max_length=100, default='Admin')
    featured_image = models.ImageField(upload_to='blog/', null=True, blank=True)
    excerpt = models.TextField(max_length=500, help_text='Brief summary of the blog post')
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    featured = models.BooleanField(default=False, help_text='Display on homepage')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Statistics
    views = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    @property
    def reading_time(self):
        """Calculate estimated reading time"""
        words = len(self.content.split())
        return max(1, words // 200)  # Average 200 words per minute
    
    def increment_views(self):
        """Increment view count"""
        self.views += 1
        self.save(update_fields=['views'])


class BlogComment(models.Model):
    """Blog Comment Model"""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.author_name} on {self.post.title}"
