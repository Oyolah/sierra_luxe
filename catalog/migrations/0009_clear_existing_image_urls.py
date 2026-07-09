# Generated migration to clear existing image URLs

from django.db import migrations


def clear_existing_image_urls(apps, schema_editor):
    """Clear existing image URLs from database to prepare for file uploads"""
    Product = apps.get_model('catalog', 'Product')
    ProductImage = apps.get_model('catalog', 'ProductImage')
    
    # Clear existing product main_image and video URLs
    Product.objects.update(main_image=None, video=None)
    
    # Clear existing product image URLs
    ProductImage.objects.update(image=None)


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_alter_product_main_image_alter_product_video_and_more'),
    ]

    operations = [
        migrations.RunPython(clear_existing_image_urls, migrations.RunPython.noop),
    ]
