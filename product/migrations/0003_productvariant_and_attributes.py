# Generated migration to add ProductVariant, Attribute, AttributeValue
from django.db import migrations, models
import uuid


def generate_sku():
    return uuid.uuid4().hex[:12].upper()


def forwards(apps, schema_editor):
    Product = apps.get_model('product', 'Product')
    ProductVariant = apps.get_model('product', 'ProductVariant')
    # If ProductVariant model doesn't exist yet in the historical models, create via ORM
    # This code will run after CreateModel operations in this migration.

    for product in Product.objects.all():
        # Use getattr for fields that might not exist in DB schema
        price = getattr(product, 'price', None)
        sale_price = getattr(product, 'sale_price', None)
        on_stock = getattr(product, 'on_stock', None) or 0
        # Create a default variant for each product
        ProductVariant.objects.create(
            product_id=product.id,
            name=f"{product.name} — Default",
            sku=generate_sku(),
            price=price if price is not None else 0,
            sale_price=sale_price if sale_price is not None and sale_price != 0 else None,
            on_stock=on_stock,
            is_default=True,
            is_active=getattr(product, 'is_active', True)
        )


def backwards(apps, schema_editor):
    # On reverse migration, move default variant data back to product if present
    Product = apps.get_model('product', 'Product')
    ProductVariant = apps.get_model('product', 'ProductVariant')
    for product in Product.objects.all():
        variant = ProductVariant.objects.filter(product_id=product.id, is_default=True).first()
        if variant:
            # Attempt to set back fields if they exist
            if hasattr(product, 'price'):
                product.price = variant.price
            if hasattr(product, 'sale_price'):
                product.sale_price = variant.sale_price or 0
            if hasattr(product, 'on_stock'):
                product.on_stock = variant.on_stock
            product.save()


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_aboutus_carousel_contactmessage_stat_support_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('attribute', models.ForeignKey(on_delete=models.CASCADE, related_name='values', to='product.attribute')),
            ],
        ),
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, help_text='Variant name e.g. Red / 128GB')),
                ('sku', models.CharField(max_length=64, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product/variants/')),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('sale_price', models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)),
                ('on_stock', models.PositiveIntegerField(default=0)),
                ('is_default', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=models.CASCADE, related_name='variants', to='product.product')),
            ],
        ),
        migrations.AddField(
            model_name='productvariant',
            name='attributes',
            field=models.ManyToManyField(blank=True, related_name='variants', to='product.attributevalue'),
        ),
        migrations.RunPython(forwards, backwards),
        # Remove legacy fields from Product if present
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sale_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_sale',
        ),
        migrations.RemoveField(
            model_name='product',
            name='out_of_stock',
        ),
        migrations.RemoveField(
            model_name='product',
            name='on_stock',
        ),
    ]
