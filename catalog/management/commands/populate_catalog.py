from django.core.management.base import BaseCommand
from django.core.files import File
from catalog.models import Category, Product, ProductImage
import os

class Command(BaseCommand):
    help = 'Populate catalog with categories and products from media files'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Women', 'slug': 'women', 'description': 'Elegant women\'s fashion'},
            {'name': 'Men', 'slug': 'men', 'description': 'Stylish men\'s fashion'},
            {'name': 'Kids', 'slug': 'kids', 'description': 'Adorable kids\' fashion'},
            {'name': 'Wedding', 'slug': 'wedding', 'description': 'Beautiful wedding attire'},
            {'name': 'Traditional', 'slug': 'traditional', 'description': 'African traditional wear'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name'], 'description': cat_data['description']}
            )
            categories[cat_data['slug']] = category
            self.stdout.write(f'{"Created" if created else "Updated"} category: {category.name}')
        
        # Product data with media files
        products_data = [
            {
                'name': 'African Lace Maxi Dress',
                'slug': 'african-lace-maxi-dress',
                'category': 'women',
                'description': 'Beautiful African lace maxi dress with intricate patterns',
                'price': 450.00,
                'stock': 10,
                'sizes': 'S, M, L, XL',
                'colors': 'Red, Blue, Green',
                'images': ['African Lace Maxi Dress 1.webp', 'African Lace Maxi Dress 2.webp', 'African Lace Maxi Dress 3.webp', 'African Lace Maxi Dress 4.webp'],
                'video': None
            },
            {
                'name': 'African Wax Print Midi Skirt',
                'slug': 'african-wax-print-midi-skirt',
                'category': 'women',
                'description': 'Stylish African wax print midi skirt',
                'price': 85.00,
                'stock': 15,
                'sizes': 'S, M, L',
                'colors': 'Multi-color',
                'images': ['african-wax-print-midi-skirt-1.avif', 'african-wax-print-midi-skirt-2.webp', 'african-wax-print-midi-skirt-3.avif', 'african-wax-print-midi-skirt-4.webp', 'african-wax-print-midi-skirt-5.avif'],
                'video': None
            },
            {
                'name': 'Aso-oke Couple Outfits',
                'slug': 'aso-oke-couple-outfits',
                'category': 'wedding',
                'description': 'Traditional Nigerian Aso-oke outfits for couples',
                'price': 550.00,
                'stock': 5,
                'sizes': 'Custom',
                'colors': 'Gold, Silver',
                'images': ['aso-oke-couple-outfits-1.webp', 'aso-oke-couple-outfits-2.webp', 'aso-oke-couple-outfits-3.webp', 'aso-oke-couple-outfits-4.webp', 'aso-oke-couple-outfits-5.webp'],
                'video': 'aso-oke-couple-outfits-video.mp4'
            },
            {
                'name': 'Baby Girl Ankara Ball Gown Dress',
                'slug': 'baby-girl-ankara-ball-gown-dress',
                'category': 'kids',
                'description': 'Adorable Ankara ball gown dress for baby girls',
                'price': 65.00,
                'stock': 20,
                'sizes': '6M, 12M, 18M',
                'colors': 'Pink, Purple',
                'images': ['baby-girl-ankara-ball-gown-dress-1.webp', 'baby-girl-ankara-ball-gown-dress-2.webp', 'baby-girl-ankara-ball-gown-dress-3.webp', 'baby-girl-ankara-ball-gown-dress-4.webp'],
                'video': 'baby-girl-ankara-ball-gown-dress-video.mp4'
            },
            {
                'name': 'Black Ball Gown for Girls',
                'slug': 'black-ball-gown-for-girls',
                'category': 'kids',
                'description': 'Elegant black ball gown for girls',
                'price': 95.00,
                'stock': 12,
                'sizes': '4, 6, 8',
                'colors': 'Black',
                'images': ['black-ball-gown-for-girls-1.avif', 'black-ball-gown-for-girls-2.avif', 'black-ball-gown-for-girls-3.jpg'],
                'video': None
            },
            {
                'name': 'Blue Lace Asoebi Dress',
                'slug': 'blue-lace-asoebi-dress',
                'category': 'wedding',
                'description': 'Beautiful blue lace Asoebi dress',
                'price': 380.00,
                'stock': 8,
                'sizes': 'S, M, L, XL',
                'colors': 'Blue',
                'images': ['blue-lace-asoebi-dress-1.avif', 'blue-lace-asoebi-dress-2.avif'],
                'video': None
            },
            {
                'name': 'Boy First Birthday Outfit',
                'slug': 'boy-first-birthday-outfit',
                'category': 'kids',
                'description': 'Stylish first birthday outfit for boys',
                'price': 75.00,
                'stock': 18,
                'sizes': '12M, 18M, 24M',
                'colors': 'Blue, White',
                'images': ['boy-first-birthday-outfit-1.webp', 'boy-first-birthday-outfit-2.webp', 'boy-first-birthday-outfit-3.webp', 'boy-first-birthday-outfit-4.webp', 'boy-first-birthday-outfit-5.webp'],
                'video': 'boy-first-birthday-outfit-video.mp4'
            },
            {
                'name': 'Brown Pencil Lace Dress',
                'slug': 'brown-pencil-lace-dress',
                'category': 'women',
                'description': 'Elegant brown pencil lace dress',
                'price': 320.00,
                'stock': 10,
                'sizes': 'S, M, L',
                'colors': 'Brown',
                'images': ['brown-pencil-lace-dress-1.avif', 'brown-pencil-lace-dress-2.avif', 'brown-pencil-lace-dress-3.avif', 'brown-pencil-lace-dress-4.avif'],
                'video': 'brown-pencil-lace-dress-video.png'
            },
            {
                'name': 'Brown Wedding Dress',
                'slug': 'brown-wedding-dress',
                'category': 'wedding',
                'description': 'Beautiful brown wedding dress',
                'price': 680.00,
                'stock': 3,
                'sizes': 'S, M, L, XL',
                'colors': 'Brown',
                'images': [f'brown-wedding-dress-image-{i}.jpg' for i in range(1, 17)],
                'video': 'brown-wedding-dress-video.mp4'
            },
            {
                'name': 'Corset Mermaid Gown Dress',
                'slug': 'corset-mermaid-gown-dress',
                'category': 'women',
                'description': 'Stunning corset mermaid gown dress',
                'price': 520.00,
                'stock': 6,
                'sizes': 'S, M, L',
                'colors': 'Red, Black',
                'images': ['corset-mermaid-gown-dress-1.webp', 'corset-mermaid-gown-dress-2.avif'],
                'video': None
            },
            {
                'name': 'Luxurious Aso-oke with Embroidered Agbada for Groom',
                'slug': 'luxurious-aso-oke-embroidered-agbada-groom',
                'category': 'men',
                'description': 'Luxurious Aso-oke with embroidered Agbada for groom',
                'price': 750.00,
                'stock': 4,
                'sizes': 'M, L, XL, XXL',
                'colors': 'Gold, Navy',
                'images': ['luxurious-aso-oke-with-embroidered-agbada-for-groom-1.avif', 'luxurious-aso-oke-with-embroidered-agbada-for-groom-2.avif', 'luxurious-aso-oke-with-embroidered-agbada-for-groom-3.webp', 'luxurious-aso-oke-with-embroidered-agbada-for-groom-4.webp', 'luxurious-aso-oke-with-embroidered-agbada-for-groom-6.avif', 'luxurious-aso-oke-with-embroidered-agbada-for-groom-7.avif', 'luxurious-aso-oke-with-embroidered-agbada-for-groom-8.avif'],
                'video': 'luxurious-aso-oke-with-embroidered-agbada-for-groom-video.mp4'
            },
            {
                'name': 'Navy Lace Asoebi Dress',
                'slug': 'navy-lace-asoebi-dress',
                'category': 'wedding',
                'description': 'Elegant navy lace Asoebi dress',
                'price': 420.00,
                'stock': 7,
                'sizes': 'S, M, L, XL',
                'colors': 'Navy',
                'images': ['navy-lace-asoebi-dress-1.webp', 'navy-lace-asoebi-dress-2.webp'],
                'video': None
            },
            {
                'name': 'Pink Pencil Lace Dress',
                'slug': 'pink-pencil-lace-dress',
                'category': 'women',
                'description': 'Beautiful pink pencil lace dress',
                'price': 350.00,
                'stock': 9,
                'sizes': 'S, M, L',
                'colors': 'Pink',
                'images': ['pink-pencil-lace-dress-1.webp', 'pink-pencil-lace-dress-2.webp', 'pink-pencil-lace-dress-3.webp', 'pink-pencil-lace-dress-4.avif', 'pink-pencil-lace-dress-5.webp'],
                'video': None
            },
            {
                'name': 'Red Beaded African Dress',
                'slug': 'red-beaded-african-dress',
                'category': 'traditional',
                'description': 'Stunning red beaded African dress',
                'price': 480.00,
                'stock': 5,
                'sizes': 'S, M, L',
                'colors': 'Red',
                'images': ['red-beaded-african-dress-1.webp', 'red-beaded-african-dress-2.webp'],
                'video': None
            },
            {
                'name': 'Red Rhinestone Wedding Dress',
                'slug': 'red-rhinestone-wedding-dress',
                'category': 'wedding',
                'description': 'Glamorous red rhinestone wedding dress',
                'price': 890.00,
                'stock': 2,
                'sizes': 'S, M, L',
                'colors': 'Red',
                'images': ['red-rhinestone-wedding-dress-1.webp', 'red-rhinestone-wedding-dress-2.webp', 'red-rhinestone-wedding-dress-3.webp'],
                'video': None
            },
        ]
        
        media_path = 'media/products/'
        
        for prod_data in products_data:
            category = categories[prod_data['category']]
            
            # Create or update product
            product, created = Product.objects.get_or_create(
                slug=prod_data['slug'],
                defaults={
                    'name': prod_data['name'],
                    'category': category,
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'stock': prod_data['stock'],
                    'sizes': prod_data['sizes'],
                    'colors': prod_data['colors'],
                    'is_active': True
                }
            )
            
            if not created:
                # Update existing product
                product.name = prod_data['name']
                product.category = category
                product.description = prod_data['description']
                product.price = prod_data['price']
                product.stock = prod_data['stock']
                product.sizes = prod_data['sizes']
                product.colors = prod_data['colors']
                product.save()
            
            # Add main image (first image)
            if prod_data['images']:
                main_image_path = os.path.join(media_path, prod_data['images'][0])
                if os.path.exists(main_image_path):
                    with open(main_image_path, 'rb') as f:
                        product.main_image.save(prod_data['images'][0], File(f), save=True)
            
            # Add video if exists
            if prod_data['video']:
                video_path = os.path.join(media_path, prod_data['video'])
                if os.path.exists(video_path):
                    with open(video_path, 'rb') as f:
                        product.video.save(prod_data['video'], File(f), save=True)
            
            # Add additional images
            for image_name in prod_data['images'][1:]:  # Skip first (already main)
                image_path = os.path.join(media_path, image_name)
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        product_image = ProductImage(product=product)
                        product_image.image.save(image_name, File(f))
                        product_image.save()
            
            self.stdout.write(f'{"Created" if created else "Updated"} product: {product.name}')
        
        self.stdout.write(self.style.SUCCESS('Catalog populated successfully!'))
