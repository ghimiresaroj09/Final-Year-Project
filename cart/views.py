from django.shortcuts import render, get_object_or_404
from .cart import Cart
from product.models import Product
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.
@login_required(login_url='login')
def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_product()
    quantities = cart.get_quantity()
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {'cart_products': cart_products, 'quantities': quantities, 'totals': totals})

@require_POST
def cart_add(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'message': 'Login required'},
            status=401
        )

    cart = Cart(request)

    product_id = int(request.POST.get('product_id'))
    product_qty = int(request.POST.get('product_qty'))

    product = get_object_or_404(Product, id=product_id)
    if product.out_of_stock or product.on_stock == 0:
        return JsonResponse({'success': False, 'message': 'This product is out of stock.'}, status=400)
    existing = cart.cart.get(str(product_id), 0)
    max_allowed = min(10, product.on_stock)
    if existing + product_qty > max_allowed:
        return JsonResponse(
            {'success': False, 'message': f'Maximum {max_allowed} allowed per product. You have {existing} in cart.'},
            status=400,
        )
    cart.add(product=product, quantity=product_qty)

    return JsonResponse({'success': True})

@login_required(login_url='login')
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get the data
        product_id = int(request.POST.get('product_id'))
        # Call delete function in Cart
        cart.delete(product_id)
        # Return response
        response = JsonResponse({'product': product_id})
        messages.success(request, "Item Deleted From Shopping Cart...")
        return response

@login_required(login_url='login')
def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        max_allowed = min(10, product.on_stock)
        if product_qty > max_allowed:
            return JsonResponse(
                {'success': False, 'message': f'Maximum {max_allowed} allowed per product.'},
                status=400,
            )
        cart.update(product_id, product_qty)
        response = JsonResponse({'qty': product_qty})
        messages.success(request, "Your Cart Has Been Updated...")
        return response
