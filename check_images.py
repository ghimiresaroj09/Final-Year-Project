import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hamroagrofarm.settings')
django.setup()

from product.models import Product

products = Product.objects.all()
print(f'Total products: {len(products)}')
print(f'\nFirst 10 products:')
for p in products[:10]:
    if p.image:
        print(f'✓ {p.name}: image={p.image.name}')
    else:
        print(f'✗ {p.name}: NO IMAGE')

print(f'\nProducts without images: {Product.objects.filter(image="").count()}')
print(f'Products with images: {Product.objects.exclude(image="").count()}')
