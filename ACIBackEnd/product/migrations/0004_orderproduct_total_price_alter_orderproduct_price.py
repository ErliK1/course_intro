# Generated by Django 5.0.7 on 2024-09-25 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_order_address_order_email_order_is_admin_order_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='total_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='price',
            field=models.FloatField(),
        ),
    ]
