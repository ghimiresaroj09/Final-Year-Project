# Generated manually for on_stock field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_productattribute_productattributevalue_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='on_stock',
            field=models.PositiveIntegerField(default=0, help_text='Available quantity in stock'),
        ),
    ]
