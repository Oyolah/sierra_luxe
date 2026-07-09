from django.core.management.base import BaseCommand
from catalog.models import Product, ProductImage, Category
from django.conf import settings

class Command(BaseCommand):
    help = 'Fix corrupted Cloudinary image URLs in database'

    def handle(self, *args, **options):
        self.stdout.write("Fixing corrupted image and video URLs...")
        
        # Fix Product main_image
        self.fix_product_images()
        
        # Fix Product videos
        self.fix_product_videos()
        
        # Fix ProductImage images
        self.fix_product_gallery_images()
        
        # Fix Category images
        self.fix_category_images()
        
        self.stdout.write(self.style.SUCCESS("Image and video URLs fixed successfully!"))

    def fix_product_images(self):
        """Fix Product main_image URLs"""
        self.stdout.write("\nFixing Product main_image fields...")
        
        products = Product.objects.all()
        fixed_count = 0
        
        for product in products:
            if product.main_image:
                original = product.main_image
                # If it's missing /image/upload/, add it
                if original.startswith('https://res.cloudinary.com/') and '/image/upload/' not in original:
                    # Extract the path after cloud name
                    parts = original.split('/')
                    if len(parts) >= 5:
                        cloud_name = parts[3]
                        path = '/'.join(parts[4:])
                        product.main_image = f"https://res.cloudinary.com/{cloud_name}/image/upload/{path}"
                        product.save()
                        fixed_count += 1
                        self.stdout.write(f"✓ Fixed: {product.name}")
                elif 'image/upload/' in original:
                    # Extract the path after image/upload/
                    if original.startswith('image/upload/'):
                        path = original.replace('image/upload/', '')
                    else:
                        path = original.split('image/upload/')[-1]
                    # Reconstruct proper Cloudinary URL
                    product.main_image = f"https://res.cloudinary.com/{settings.CLOUDINARY_STORAGE['CLOUD_NAME']}/image/upload/{path}"
                    product.save()
                    fixed_count += 1
                    self.stdout.write(f"✓ Fixed: {product.name}")
                elif not original.startswith('https://'):
                    # If it's just a path, construct full URL
                    product.main_image = f"https://res.cloudinary.com/{settings.CLOUDINARY_STORAGE['CLOUD_NAME']}/image/upload/{original}"
                    product.save()
                    fixed_count += 1
                    self.stdout.write(f"✓ Fixed: {product.name}")
        
        self.stdout.write(f"Fixed {fixed_count} product main images")

    def fix_product_videos(self):
        """Fix Product video URLs"""
        self.stdout.write("\nFixing Product video fields...")
        
        products = Product.objects.all()
        fixed_count = 0
        
        for product in products:
            if product.video:
                original = product.video
                # If it's missing /video/upload/, add it
                if original.startswith('https://res.cloudinary.com/') and '/video/upload/' not in original:
                    parts = original.split('/')
                    if len(parts) >= 5:
                        cloud_name = parts[3]
                        path = '/'.join(parts[4:])
                        product.video = f"https://res.cloudinary.com/{cloud_name}/video/upload/{path}"
                        product.save()
                        fixed_count += 1
                        self.stdout.write(f"✓ Fixed video: {product.name}")
                elif 'video/upload/' in original:
                    if original.startswith('video/upload/'):
                        path = original.replace('video/upload/', '')
                    else:
                        path = original.split('video/upload/')[-1]
                    product.video = f"https://res.cloudinary.com/{settings.CLOUDINARY_STORAGE['CLOUD_NAME']}/video/upload/{path}"
                    product.save()
                    fixed_count += 1
                    self.stdout.write(f"✓ Fixed video: {product.name}")
                elif not original.startswith('https://'):
                    product.video = f"https://res.cloudinary.com/{settings.CLOUDINARY_STORAGE['CLOUD_NAME']}/video/upload/{original}"
                    product.save()
                    fixed_count += 1
                    self.stdout.write(f"✓ Fixed video: {product.name}")
        
        self.stdout.write(f"Fixed {fixed_count} product videos")

    def fix_product_gallery_images(self):
        """Fix ProductImage image URLs"""
        self.stdout.write("\nFixing ProductImage fields...")
        
        product_images = ProductImage.objects.all()
        fixed_count = 0
        
        for img in product_images:
            if img.image:
                original = img.image
                # If it's missing /image/upload/, add it
                if original.startswith('https://res.cloudinary.com/') and '/image/upload/' not in original:
                    parts = original.split('/')
                    if len(parts) >= 5:
                        cloud_name = parts[3]
                        path = '/'.join(parts[4:])
                        img.image = f"https://res.cloudinary.com/{cloud_name}/image/upload/{path}"
                        img.save()
                        fixed_count += 1
                        self.stdout.write(f"✓ Fixed: {img.product.name} - {img.id}")
                elif 'image/upload/' in original:
                    if original.startswith('image/upload/'):
                        path = original.replace('image/upload/', '')
                    else:
                        path = original.split('image/upload/')[-1]
                    img.image = f"https://res.cloudinary.com/{settings.CLOUDINARY_STORAGE['CLOUD_NAME']}/image/upload/{path}"
                    img.save()
                    fixed_count += 1
                    self.stdout.write(f"✓ Fixed: {img.product.name} - {img.id}")
                elif not original.startswith('https://'):
                    img.image = f"https://res.cloudinary.com/{settings.CLOUDINARY_STORAGE['CLOUD_NAME']}/image/upload/{original}"
                    img.save()
                    fixed_count += 1
                    self.stdout.write(f"✓ Fixed: {img.product.name} - {img.id}")
        
        self.stdout.write(f"Fixed {fixed_count} product gallery images")

    def fix_category_images(self):
        """Fix Category image URLs"""
        self.stdout.write("\nFixing Category images...")
        
        categories = Category.objects.all()
        fixed_count = 0
        
        for category in categories:
            if category.image:
                original = category.image
                if 'image/upload/' in original:
                    if original.startswith('image/upload/'):
                        path = original.replace('image/upload/', '')
                    else:
                        path = original.split('image/upload/')[-1]
                    category.image = f"https://res.cloudinary.com/{settings.CLOUDINARY_STORAGE['CLOUD_NAME']}/image/upload/{path}"
                    category.save()
                    fixed_count += 1
                    self.stdout.write(f"✓ Fixed: {category.name}")
                elif not original.startswith('https://'):
                    category.image = f"https://res.cloudinary.com/{settings.CLOUDINARY_STORAGE['CLOUD_NAME']}/image/upload/{original}"
                    category.save()
                    fixed_count += 1
                    self.stdout.write(f"✓ Fixed: {category.name}")
        
        self.stdout.write(f"Fixed {fixed_count} category images")
