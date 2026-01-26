from django.shortcuts import render, HttpResponse, redirect
from .models import *
from blog.models import BlogPost
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import F


# Create your views here.
def product_catalog(request):
    categories= Category.objects.all().order_by('name')
    # Paginate categories with 4 categories per page
    paginator = Paginator(categories, 3)
    page_number = request.GET.get('page')  # Get the page number from the query parameter 'page'
    page_obj = paginator.get_page(page_number)
    catwise={}
    for category in page_obj:
        product=Product.objects.filter(category=category).order_by('out_of_stock')
        catwise[category]= product
    return render(request,'product.html',{'catwise':catwise,'page_obj':page_obj})


def product(request, pk):
    try:
        product=Product.objects.get(id=pk)
        related_products=Product.objects.filter(category=product.category).exclude(id=product.id).order_by('?')[:4]
        return render(request,'product_detail.html',{'product':product,'related_products':related_products})
    except:
        return render(request, '404notfound.html')


def category(request, cname):
    try:
        category = Category.objects.get(name=cname)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products,'category':category})
    except:
        return render(request, '404notfound.html')

@login_required(login_url='login')
def add_product(request):
    if request.user.is_authenticated and request.user.is_superuser:
        product=""
        if request.method == 'POST' or request.method== "FILES":
            name = request.POST['name']
            price = request.POST['price']
            description = request.POST['description']
            category_id = request.POST['category']
            image = request.FILES['image']

            # Fetch the Category instance
            category = Category.objects.get(id=category_id)
            
            product = Product.objects.create(name=name, price=price, description=description, category=category, image=image)
            product.save()
            messages.success(request, 'Product Added Successfully')
            return redirect('product_catalog')
        
        return render(request,'add_product.html',{'product':product})
    else:
        messages.error(request, "Access Denied")
        return redirect('product_catalog')

def search(request):
    query = request.GET.get('query', '')
    if query:
        products = Product.objects.filter(name__icontains=query)    #The icontains lookup is used to get records that contains a specified value.
    else:
        products = Product.objects.none()
    return render(request, 'search_results.html', {'products': products, 'query': query})


def sale(request):
    products=Product.objects.filter(is_sale=True).order_by('sale_price')
    return render(request,'sale.html',{'products':products})


def home(request):
    """Homepage landing page view"""
    carousels = Carousel.objects.filter(is_active=True)
    about_us = AboutUs.objects.filter(is_active=True).first()
    stats = Stat.objects.filter(is_active=True)
    
    # Get top 4 products with highest savings (on sale)
    # Use F expressions to calculate savings in the database query
    top_sales = Product.objects.filter(is_sale=True, out_of_stock=False).annotate(
        savings_amount=F('price') - F('sale_price')
    ).order_by('-savings_amount')[:4]
    
    # Get featured blogs
    featured_blogs = BlogPost.objects.filter(status='published', featured=True).order_by('-published_at')[:3]
    
    # Get testimonials
    testimonials = Testimonial.objects.filter(is_active=True)
    
    # Get team members
    team_members = TeamMember.objects.filter(is_active=True)
    
    # Get support information
    support = Support.objects.filter(is_active=True).first()
    
    context = {
        'carousels': carousels,
        'about_us': about_us,
        'stats': stats,
        'top_sales': top_sales,
        'featured_blogs': featured_blogs,
        'testimonials': testimonials,
        'team_members': team_members,
        'support': support,
    }
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('home')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'home.html', context)