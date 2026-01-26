from django.shortcuts import render, HttpResponse, redirect
from .models import *
from blog.models import BlogPost
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


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


@csrf_exempt
def chatbot(request):
    """AI Chatbot endpoint that responds to queries about database information"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '').lower().strip()
            
            if not message:
                return JsonResponse({'response': 'Please ask me something about our products, team, sales, or stats!'})
            
            response = ""
            
            # Check for product-related queries
            product_keywords = ['product', 'item', 'buy', 'price', 'cost', 'available', 'stock', 'category', 'categories']
            team_keywords = ['team', 'member', 'staff', 'employee', 'who', 'people', 'person']
            sales_keywords = ['sale', 'discount', 'offer', 'cheap', 'affordable', 'deal', 'promotion']
            stats_keywords = ['stat', 'statistic', 'number', 'count', 'total', 'how many', 'customers', 'experience']
            
            message_lower = message.lower()
            
            # Product queries
            if any(keyword in message_lower for keyword in product_keywords):
                # Check for specific product name
                products = Product.objects.filter(out_of_stock=False)
                for product in products:
                    if product.name.lower() in message_lower:
                        response = f"<strong>{product.name}</strong><br>"
                        response += f"Price: Rs. {product.sale_price if product.is_sale else product.price}<br>"
                        if product.is_sale:
                            response += f"<s>Original Price: Rs. {product.price}</s><br>"
                            response += f"<span style='color: #dc3545;'>Save Rs. {product.savings}</span><br>"
                        response += f"Stock: {product.on_stock} available<br>"
                        response += f"Category: {product.category.name}<br>"
                        if product.description:
                            response += f"Description: {product.description}<br>"
                        response += f"<a href='/product/{product.id}' style='color: #0db04b; text-decoration: underline;'>View Product</a>"
                        return JsonResponse({'response': response})
                
                # Check for category
                categories = Category.objects.all()
                for category in categories:
                    if category.name.lower() in message_lower:
                        products_in_cat = Product.objects.filter(category=category, out_of_stock=False)
                        response = f"<strong>Products in {category.name}:</strong><br>"
                        if products_in_cat.exists():
                            for p in products_in_cat[:5]:
                                response += f"• {p.name} - Rs. {p.sale_price if p.is_sale else p.price}<br>"
                            if products_in_cat.count() > 5:
                                response += f"<br>...and {products_in_cat.count() - 5} more. <a href='/category/{category.name}' style='color: #0db04b;'>View all</a>"
                        else:
                            response += "No products available in this category."
                        return JsonResponse({'response': response})
                
                # General product list
                all_products = Product.objects.filter(out_of_stock=False)[:10]
                if all_products.exists():
                    response = f"<strong>Available Products:</strong><br>"
                    for product in all_products:
                        price = product.sale_price if product.is_sale else product.price
                        sale_badge = " <span style='color: #dc3545;'>[SALE]</span>" if product.is_sale else ""
                        response += f"• {product.name} - Rs. {price}{sale_badge}<br>"
                    response += "<br><a href='/products/' style='color: #0db04b;'>View all products</a>"
                else:
                    response = "Sorry, no products are currently available."
            
            # Team member queries
            elif any(keyword in message_lower for keyword in team_keywords):
                team_members = TeamMember.objects.filter(is_active=True).order_by('order', 'name')
                if team_members.exists():
                    response = "<strong>Our Team:</strong><br>"
                    for member in team_members:
                        response += f"<strong>{member.name}</strong> - {member.position}<br>"
                        if member.bio:
                            response += f"{member.bio[:100]}...<br>"
                        response += "<br>"
                else:
                    response = "Our team information is not available at the moment."
            
            # Sales queries
            elif any(keyword in message_lower for keyword in sales_keywords):
                sale_products = Product.objects.filter(is_sale=True, out_of_stock=False).annotate(
                    savings_amount=F('price') - F('sale_price')
                ).order_by('-savings_amount')[:10]
                if sale_products.exists():
                    response = "<strong>Products on Sale:</strong><br>"
                    for product in sale_products:
                        response += f"• <strong>{product.name}</strong><br>"
                        response += f"  Price: <s>Rs. {product.price}</s> <span style='color: #dc3545;'>Rs. {product.sale_price}</span><br>"
                        response += f"  Save: Rs. {product.savings}<br><br>"
                    response += "<a href='/sale/' style='color: #0db04b;'>View all sales</a>"
                else:
                    response = "Currently, there are no products on sale."
            
            # Stats queries
            elif any(keyword in message_lower for keyword in stats_keywords):
                stats = Stat.objects.filter(is_active=True).order_by('order')
                if stats.exists():
                    response = "<strong>Our Statistics:</strong><br>"
                    for stat in stats:
                        response += f"<strong>{stat.get_stat_type_display()}:</strong> {stat.value}+<br>"
                        if stat.label:
                            response += f"{stat.label}<br>"
                        response += "<br>"
                else:
                    response = "Statistics are not available at the moment."
            
            # Greeting or help
            elif any(word in message_lower for word in ['hi', 'hello', 'hey', 'help', 'what can you do']):
                response = "Hello! I'm your AI assistant. I can help you with:<br>"
                response += "• <strong>Products</strong> - Ask about products, prices, categories, or stock<br>"
                response += "• <strong>Sales</strong> - Ask about discounts and offers<br>"
                response += "• <strong>Team</strong> - Ask about our team members<br>"
                response += "• <strong>Stats</strong> - Ask about our statistics<br><br>"
                response += "Try asking: 'What products do you have?', 'Show me sales', 'Tell me about your team', or 'What are your stats?'"
            
            # Default response
            else:
                response = "I can help you with information about our products, sales, team members, and statistics. "
                response += "Try asking: 'What products do you have?', 'Show me sales', 'Tell me about your team', or 'What are your stats?'"
            
            return JsonResponse({'response': response})
            
        except Exception as e:
            return JsonResponse({'response': f'Sorry, I encountered an error. Please try again. Error: {str(e)}'}, status=500)
    
    return JsonResponse({'response': 'Please send a POST request with your message.'}, status=400)