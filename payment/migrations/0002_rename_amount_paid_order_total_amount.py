# Generated by Django 5.0 on 2024-08-10 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='amount_paid',
            new_name='total_amount',
        ),
    ]
