# Generated by Django 2.2 on 2020-01-08 18:01

from django.db import migrations, models
import shopping.models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0004_auto_20200108_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image2',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=shopping.models.upload_image_path),
        ),
    ]
