from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib import messages
import json
from cart.cart import Cart

# Custom Password Reset View for HTML Emails
class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        """
        Send a password reset email with HTML formatting
        """
        from django.conf import settings
        from django.http import HttpResponseRedirect
        
        # Get the user from the form
        for user in form.get_users(form.cleaned_data['email']):
            # Generate token and UID
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Build the reset URL
            protocol = 'https' if self.request.is_secure() else 'http'
            domain = self.request.get_host()
            reset_url = f"{protocol}://{domain}/user/password_reset_confirm/{uid}/{token}/"
            
            # Prepare context for email templates
            context = {
                'user': user,
                'protocol': protocol,
                'domain': domain,
                'uid': uid,
                'token': token,
                'reset_url': reset_url,
            }
            
            # Render HTML and text versions
            try:
                html_message = render_to_string('registration/password_reset_email.html', context)
            except:
                html_message = None
            
            text_message = render_to_string('registration/password_reset_email.txt', context)
            
            # Create multipart email (HTML + Plain Text)
            email = EmailMultiAlternatives(
                subject='Password Reset Request - Hamro Agro Farm',
                body=text_message,  # Plain text version as fallback
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email]
            )
            
            # Attach HTML version
            if html_message:
                email.attach_alternative(html_message, "text/html")
            
            # Send email
            email.send(fail_silently=False)
        
        # Redirect to password reset done page (don't call super() to avoid duplicate emails)
        return HttpResponseRedirect(self.get_success_url())

# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me',False)  # Get the "Remember Me" checkbox value

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Handle Remember Me functionality
            if not remember_me:
                request.session.set_expiry(0)  # Session expires when the browser closes
            else:
                request.session.set_expiry(1209600)  # Set session expiry to 2 weeks (in seconds)

            # Retrieve saved cart from user's profile and load into the session
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')
    else:
        return render(request, 'login.html', {})

    
def register_user(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        #Check if password and confirm_password is same or not
        if password != confirm_password:
            messages.warning(request, "Password and Confirm Password does not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already taken.")
            return redirect('register')

        # If the user doesn't exist, proceed with creating a new user
        my_user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name)
        my_user.set_password(password)
        try:
            my_user.save()
            login(request, my_user)   #This will directly log the user immediately after registering.
            messages.success(request, "You have been registered successfully!!!")
            return redirect('update_info')
        except:
            messages.error(request, "Error while registering!!!")

    return render(request, 'register.html')

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out!!!"))
    return redirect('home')

@login_required(login_url='login')
def view_profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

@login_required(login_url='login')
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        user.first_name= request.POST.get('first_name')
        user.last_name= request.POST.get('last_name')
        user.email= request.POST.get('email')
        user.save()
        messages.success(request,("Your profile have been updated successfully!!!"))
        return redirect('view_profile')
    return render(request, 'edit_profile.html', {'user': user})

@login_required(login_url='login')
def delete_profile(request):
    user = request.user
    if request.method=='POST':
        user.delete()
        messages.error(request,("Your profile have been deleted successfully!!!"))
        return redirect('home')
    return render(request, 'delete_profile.html', {'user': user})


@login_required
def update_info(request):
    if request.method == "POST":
        profile = Profile.objects.get(user__id=request.user.id)
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('home')
    else:
        profile = Profile.objects.get(user=request.user)
    
    return render(request, 'info.html', {'profile': profile})