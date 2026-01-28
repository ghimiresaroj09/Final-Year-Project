from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from product.models import Product


# Create Order Model
class Order(models.Model):
    class ShippingStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SHIPPED = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'
    
    # Foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    phone = models.CharField(max_length=15, blank=True, null=True)
    shipping_address = models.TextField(max_length=15000)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_ordered = models.DateTimeField(auto_now_add=True)    
    shipping_status = models.CharField(max_length=20, choices=ShippingStatus.choices, default=ShippingStatus.PENDING)
    date_shipped = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Order  by  {str(self.full_name)}  on  {self.date_ordered.strftime("%Y-%m-%d")}  of  Rs.{self.total_amount}  from  {self.shipping_address}'
    
    def save(self, *args, **kwargs):
        # Check if the shipping_status is being marked as SHIPPED
        if self.shipping_status == self.ShippingStatus.SHIPPED and not self.date_shipped:
            self.date_shipped = timezone.now()  # Correct usage of timezone.now()
        elif self.shipping_status != self.ShippingStatus.SHIPPED:
            self.date_shipped = None  # Reset the date if shipping status is not SHIPPED

        super().save(*args, **kwargs)


# Create Order Item Model
class OrderItem(models.Model):
    # Foreign Keys
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{str(self.product)} of Order Id: {self.order.id}'

    def save(self, *args, **kwargs):
        # Calculate subtotal
        self.subtotal = self.unit_price * self.quantity
        super().save(*args, **kwargs)
