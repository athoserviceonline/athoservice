# Generated by Django 2.2 on 2020-01-09 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0008_product_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
