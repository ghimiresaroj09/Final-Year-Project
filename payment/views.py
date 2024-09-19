from datetime import datetime
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from product.models import Product
from cart.cart import Cart
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

@login_required
def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        # Get user information from request
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        shipping_address = request.POST.get('shipping_address')

        # Create Order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            shipping_address=shipping_address,
            total_amount=cart.cart_total(),  # Calculate total amount
        )

        # Create Order Items
        for product_id, quantity in cart.get_quantity().items():
            product = get_object_or_404(Product, id=product_id)
            unit_price = product.sale_price if product.is_sale else product.price
            OrderItem.objects.create(
                order=order,
                product=product,
                user=request.user,
                quantity=quantity,
                unit_price=unit_price,
                subtotal=unit_price * quantity,
            )

        order_items = OrderItem.objects.filter(order=order)

        # Prepare and send email
        subject = 'New Order Alert'
        html_content = render_to_string('order_alert_email.html', {
            'order': order,
            'order_items': order_items,
        })
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email='hamroagrofarm@gmail.com',
            to=['hamroagrofarm@gmail.com'],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        # Clear the session cart
        request.session['cart'] = {}
        
        # Clear the old_cart in the user's profile
        if request.user.is_authenticated:
            profile = request.user.profile  # Assuming the Profile model is linked with a OneToOneField to the User model
            profile.old_cart = "{}"  # Set it to an empty dictionary (or None)
            profile.save()

        messages.success(request, 'Your order has been placed successfully, and an email has been sent to the owner.')

        # Redirect to the order confirmation page
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'checkout.html')



@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'order_confirmation.html', context)


@login_required
def order_history(request):
    # Fetch all orders for the current user
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    context = {
        'orders': orders,
    }
    return render(request, 'order_history.html', context)

@login_required
def unshipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipping_status=False).order_by('-date_ordered')
        if request.method == 'POST':
            order_id = request.POST['num']
            # Get the order or return 404 if not found
            order = get_object_or_404(Order, id=order_id)
            # Update the order
            order.shipping_status = True
            order.date_shipped = datetime.now()
            order.save()
            # Redirect with success message
            messages.success(request, "Shipping Status Updated")
            return redirect('unshipped_dash')

        return render(request, "unshipped_dash.html", {"orders": orders})
    else:
        messages.error(request, "Access Denied")
        return redirect('home')

@login_required
def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipping_status=True).order_by('-date_ordered')
        if request.method == 'POST':
            order_id = request.POST['num']
            # Get the order or return 404 if not found
            order = get_object_or_404(Order, id=order_id)
            # Update the order
            order.shipping_status = False
            order.date_shipped = None  # Reset the shipped date
            order.save()
            # Redirect with success message
            messages.success(request, "Shipping Status Updated")
            return redirect('shipped_dash')

        return render(request, "shipped_dash.html", {"orders": orders})
    else:
        messages.error(request, "Access Denied")
        return redirect('home')
    


@login_required
def generate_invoice_pdf(request, order_id):
    if request.user.is_superuser:
        order = get_object_or_404(Order, id=order_id)
        order_items = OrderItem.objects.filter(order=order)

        # Load the invoice template
        template_path = 'invoice.html'
        context = {
            'order': order,
            'order_items': order_items,
        }

        # Render the HTML template to a string
        template = get_template(template_path)
        html = template.render(context)

        # Create a PDF from the rendered HTML
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

        # Use xhtml2pdf to convert HTML to PDF
        pisa_status = pisa.CreatePDF(html, dest=response)

        # Return PDF file if successfully created, else return an error
        if pisa_status.err:
            return HttpResponse('Error creating PDF', status=400)

        return response
    else:
        messages.error(request, "Access Denied")
        return redirect('home')
