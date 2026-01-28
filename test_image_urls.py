import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hamroagrofarm.settings')
django.setup()

from product.models import Product
from django.template.loader import render_to_string
from django.template import Context

# Get first product
product = Product.objects.first()
if product:
    print(f"Product: {product.name}")
    print(f"Product image field: {product.image}")
    print(f"Product image.name: {product.image.name}")
    print(f"Product image.url: {product.image.url}")
    print(f"\nTemplate render test:")
    print(f"{{ product.image.url }} would render as: {product.image.url}")
else:
    print("No products found")
