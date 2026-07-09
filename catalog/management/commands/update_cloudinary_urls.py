from django.core.management.base import BaseCommand
from catalog.models import Product, ProductImage, Category
from django.conf import settings

class Command(BaseCommand):
    help = 'Update database with Cloudinary URLs for existing images'

    def handle(self, *args, **options):
        self.stdout.write("Updating Cloudinary URLs in database")
        self.stdout.write("=" * 60)
        
        # Update Product main_image
        self.update_product_images()
        
        # Update ProductImage images
        self.update_product_gallery_images()
        
        # Update Category images
        self.update_category_images()
        
        self.stdout.write(self.style.SUCCESS("\nDatabase update completed!"))

    def update_product_images(self):
        """Update Product main_image with Cloudinary URLs"""
        self.stdout.write("\nUpdating Product main_image fields...")
        
        products = Product.objects.all()
        updated_count = 0
        
        for product in products:
            if product.main_image:
                # Get the filename from the current image path
                old_path = str(product.main_image)
                if old_path and not old_path.startswith('http'):
                    # Extract filename from path
                    filename = old_path.split('/')[-1]
                    # Create Cloudinary URL
                    cloudinary_url = f"https://res.cloudinary.com/{settings.CLOUDINARY_STORAGE['CLOUD_NAME']}/image/upload/v1/sierra_luxe/products/{filename}"
                    
                    # Update the field
                    product.main_image = cloudinary_url
                    product.save()
                    updated_count += 1
                    self.stdout.write(f"✓ Updated: {product.name}")
        
        self.stdout.write(f"Updated {updated_count} product main images")

    def update_product_gallery_images(self):
        """Update ProductImage images with Cloudinary URLs"""
        self.stdout.write("\nUpdating ProductImage fields...")
        
        product_images = ProductImage.objects.all()
        updated_count = 0
        
        for img in product_images:
            if img.image:
                old_path = str(img.image)
                if old_path and not old_path.startswith('http'):
                    filename = old_path.split('/')[-1]
                    cloudinary_url = f"https://res.cloudinary.com/{settings.CLOUDINARY_STORAGE['CLOUD_NAME']}/image/upload/v1/sierra_luxe/products/{filename}"
                    
                    img.image = cloudinary_url
                    img.save()
                    updated_count += 1
                    self.stdout.write(f"✓ Updated: {img.product.name} - {img.id}")
        
        self.stdout.write(f"Updated {updated_count} product gallery images")

    def update_category_images(self):
        """Update Category images with Cloudinary URLs"""
        self.stdout.write("\nUpdating Category images...")
        
        categories = Category.objects.all()
        updated_count = 0
        
        for category in categories:
            if category.image:
                old_path = str(category.image)
                if old_path and not old_path.startswith('http'):
                    filename = old_path.split('/')[-1]
                    cloudinary_url = f"https://res.cloudinary.com/{settings.CLOUDINARY_STORAGE['CLOUD_NAME']}/image/upload/v1/sierra_luxe/categories/{filename}"
                    
                    category.image = cloudinary_url
                    category.save()
                    updated_count += 1
                    self.stdout.write(f"✓ Updated: {category.name}")
        
        self.stdout.write(f"Updated {updated_count} category images")
