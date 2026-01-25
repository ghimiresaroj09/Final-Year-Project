# Blog App Setup Guide

## Installation Steps

### 1. **Add 'blog' to INSTALLED_APPS**
Edit `hamroagrofarm/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Your apps
    'product',
    'cart',
    'payment',
    'user',
    'blog',  # ← Add this line
]
```

### 2. **Add Blog URLs to Main URLs**
Edit `hamroagrofarm/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('product/', include('product.urls')),
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls')),
    path('user/', include('user.urls')),
    path('blog/', include('blog.urls')),  # ← Add this line
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 3. **Add Context Processor (Optional)**
Edit `hamroagrofarm/settings.py` - Find `TEMPLATES` section:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'product.context_processor.categories',
                'cart.context_processor.cart',
                'blog.context_processors.blog_context',  # ← Add this line
            ],
        },
    },
]
```

### 4. **Create Migrations**
Run in terminal:

```bash
python manage.py makemigrations blog
python manage.py migrate blog
```

### 5. **Create Superuser (if needed)**
```bash
python manage.py createsuperuser
```

### 6. **Add Blog Link to Navbar (Optional)**
Edit `templates/navbar.html`, find the navigation links and add:

```html
<li class="nav-item">
  <a class="nav-link" href="{% url 'blog:blog_list' %}">
    <i class="bi bi-journal-text me-1"></i>Blog
  </a>
</li>
```

## Features

### Models
- **Category**: Blog categories with icons and descriptions
- **BlogPost**: Main blog model with:
  - Auto slug generation
  - Featured/draft status
  - View counter
  - Auto reading time calculation
  - SEO meta descriptions
  - Image support
  
- **BlogComment**: User comments on blog posts (with approval system)

### Views
- **blog_list**: Display all published posts with:
  - Pagination (6 posts per page)
  - Category filtering
  - Search functionality
  - Featured posts sidebar
  
- **blog_detail**: Single post view with:
  - Auto view counting
  - Related posts
  - Comments display
  - Reading time calculation

### Admin Interface
Full Django admin integration with:
- Slug auto-generation
- Category management
- Comment moderation
- Status/featured management

## Usage

### 1. **Create Blog Categories**
Go to `/admin/blog/category/` and create categories like:
- Tips & Tricks
- Product News
- Farming Guide
- Seasonal Updates

### 2. **Create Blog Posts**
Go to `/admin/blog/blogpost/` and create posts:
- Write content (supports HTML)
- Upload featured image
- Set category
- Mark as published
- Optionally set as featured

### 3. **Manage Comments**
Go to `/admin/blog/blogcomment/` to:
- Review user comments
- Approve/reject comments
- Delete spam

## URLs

- **Blog List**: `/blog/`
  - Filter by category: `/blog/?category=tips-tricks`
  - Search: `/blog/?search=organic`
  
- **Blog Detail**: `/blog/post-slug/`

## Customization

### Change Posts Per Page
Edit `blog/views.py`, line 23:
```python
paginator = Paginator(posts, 6)  # Change 6 to desired number
```

### Change Featured Posts Count
Edit `blog/views.py`, line 30:
```python
).order_by('-published_at')[:3]  # Change 3 to desired number
```

### Change Reading Time Calculation
Edit `blog/models.py`, line 58:
```python
return max(1, words // 200)  # 200 = words per minute
```

## File Structure

```
blog/
├── __init__.py
├── admin.py           # Admin configuration
├── apps.py            # App configuration
├── context_processors.py  # Global context variables
├── forms.py           # Comment form
├── models.py          # BlogPost, Category, Comment models
├── tests.py           # Unit tests
├── urls.py            # URL routing
├── views.py           # Blog list & detail views
├── migrations/        # Database migrations
└── templates/
    └── blog/
        ├── blog_list.html     # Blog listing page
        └── blog_detail.html   # Individual post page
```

## Database Schema

```sql
-- Categories
blog_category
- id (PK)
- name
- slug
- description
- icon

-- Blog Posts
blog_blogpost
- id (PK)
- title
- slug
- category_id (FK)
- author
- featured_image
- excerpt
- content
- status
- featured
- created_at
- updated_at
- published_at
- meta_description
- views

-- Comments
blog_blogcomment
- id (PK)
- post_id (FK)
- author_name
- author_email
- content
- is_approved
- created_at
```

## Tips

1. **SEO Optimization**: Fill in `meta_description` for better search engine rankings
2. **Featured Images**: Use 1200x600 px images for best appearance
3. **Content Format**: Support basic HTML in content field
4. **Categories**: Limit to 5-7 categories for better organization
5. **Publishing**: Always set status to 'Published' to make posts visible
6. **Comments**: Enable comment moderation to prevent spam

## Troubleshooting

### Blog page shows 404
- Check if 'blog' is in INSTALLED_APPS
- Check if blog URLs are included in main urls.py
- Run migrations: `python manage.py migrate`

### Images not showing
- Ensure MEDIA_URL and MEDIA_ROOT are configured in settings.py
- Images should be in `media/blog/` folder
- Check file permissions

### Pagination not working
- Ensure page parameter is in GET request
- Check if page_obj is being passed to template

---

**Blog App Created Successfully!** 🎉
Your blog system is now ready to use. Start adding categories and posts through the Django admin panel.
