from django.core.management.base import BaseCommand
from catalog.models import Product, ProductImage, Category
from django.conf import settings

class Command(BaseCommand):
    help = 'Fix corrupted Cloudinary image URLs in database'

    def handle(self, *args, **options):
        self.stdout.write("Fixing corrupted image and video URLs...")
        self.cloud_name = settings.CLOUDINARY_STORAGE['CLOUD_NAME']
        
        self.fix_product_images()
        self.fix_product_videos()
        self.fix_product_gallery_images()
        self.fix_category_images()
        
        self.stdout.write(self.style.SUCCESS("Image and video URLs fixed successfully!"))

    def fix_url(self, url, resource_type='image', include_sierra_luxe=False):
        """Generic URL fixer for Cloudinary URLs"""
        if not url:
            return url
            
        # Already correct with version and sierra_luxe
        if url.startswith(f'https://res.cloudinary.com/{self.cloud_name}/{resource_type}/upload/v') and (not include_sierra_luxe or '/sierra_luxe/' in url):
            return url
        
        # Has full URL with /resource_type/upload/ but missing version or sierra_luxe
        if url.startswith(f'https://res.cloudinary.com/{self.cloud_name}/{resource_type}/upload/'):
            # Check if needs sierra_luxe folder
            if include_sierra_luxe:
                # Has /v1/products/ but needs /v1/sierra_luxe/products/
                if f'/{resource_type}/upload/v1/products/' in url:
                    return url.replace(f'/{resource_type}/upload/v1/products/', f'/{resource_type}/upload/v1/sierra_luxe/products/')
                # Has /products/ but missing version and sierra_luxe
                elif f'/{resource_type}/upload/products/' in url:
                    return url.replace(f'/{resource_type}/upload/products/', f'/{resource_type}/upload/v1/sierra_luxe/products/')
                # Has /resource_type/upload/ but missing version and sierra_luxe
                elif f'/{resource_type}/upload/v' not in url:
                    path = url.split(f'/{resource_type}/upload/')[-1]
                    return f"https://res.cloudinary.com/{self.cloud_name}/{resource_type}/upload/v1/sierra_luxe/{path}"
            return url
        
        # Has full URL but missing /resource_type/upload/
        if url.startswith('https://res.cloudinary.com/') and f'/{resource_type}/upload/' not in url:
            parts = url.split('/')
            if len(parts) >= 5:
                path = '/'.join(parts[4:])
                prefix = f'/v1/sierra_luxe/' if include_sierra_luxe else '/'
                return f"https://res.cloudinary.com/{self.cloud_name}/{resource_type}/upload{prefix}{path}"
        
        # Has partial path with resource_type/upload/
        if f'{resource_type}/upload/' in url and not url.startswith('https://'):
            path = url.split(f'{resource_type}/upload/')[-1]
            prefix = f'v1/sierra_luxe/' if include_sierra_luxe else ''
            return f"https://res.cloudinary.com/{self.cloud_name}/{resource_type}/upload/{prefix}{path}"
        
        # Just a path
        if not url.startswith('https://'):
            prefix = f'v1/sierra_luxe/' if include_sierra_luxe else ''
            return f"https://res.cloudinary.com/{self.cloud_name}/{resource_type}/upload/{prefix}{url}"
        
        return url

    def fix_product_images(self):
        """Fix Product main_image URLs"""
        self.stdout.write("\nFixing Product main_image fields...")
        fixed_count = 0
        
        for product in Product.objects.all():
            if product.main_image:
                fixed_url = self.fix_url(product.main_image, 'image')
                if fixed_url != product.main_image:
                    product.main_image = fixed_url
                    product.save()
                    fixed_count += 1
                    self.stdout.write(f"✓ Fixed: {product.name}")
        
        self.stdout.write(f"Fixed {fixed_count} product main images")

    def fix_product_videos(self):
        """Fix Product video URLs"""
        self.stdout.write("\nFixing Product video fields...")
        fixed_count = 0
        
        for product in Product.objects.all():
            if product.video:
                fixed_url = self.fix_url(product.video, 'video', include_sierra_luxe=True)
                if fixed_url != product.video:
                    product.video = fixed_url
                    product.save()
                    fixed_count += 1
                    self.stdout.write(f"✓ Fixed video: {product.name}")
        
        self.stdout.write(f"Fixed {fixed_count} product videos")

    def fix_product_gallery_images(self):
        """Fix ProductImage image URLs"""
        self.stdout.write("\nFixing ProductImage fields...")
        fixed_count = 0
        
        for img in ProductImage.objects.all():
            if img.image:
                fixed_url = self.fix_url(img.image, 'image')
                if fixed_url != img.image:
                    img.image = fixed_url
                    img.save()
                    fixed_count += 1
                    self.stdout.write(f"✓ Fixed: {img.product.name} - {img.id}")
        
        self.stdout.write(f"Fixed {fixed_count} product gallery images")

    def fix_category_images(self):
        """Fix Category image URLs"""
        self.stdout.write("\nFixing Category images...")
        fixed_count = 0
        
        for category in Category.objects.all():
            if category.image:
                fixed_url = self.fix_url(category.image, 'image')
                if fixed_url != category.image:
                    category.image = fixed_url
                    category.save()
                    fixed_count += 1
                    self.stdout.write(f"✓ Fixed: {category.name}")
        
        self.stdout.write(f"Fixed {fixed_count} category images")
