# Generated by Django 4.2.7 on 2023-12-09 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_alter_orderitem_subtotal_delete_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
    ]