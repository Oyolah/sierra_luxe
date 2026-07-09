from django.core.management.base import BaseCommand
import cloudinary
import cloudinary.uploader
from pathlib import Path
from django.conf import settings

class Command(BaseCommand):
    help = 'Upload existing media files to Cloudinary'

    def handle(self, *args, **options):
        # Configure Cloudinary
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
            api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
            api_secret=settings.CLOUDINARY_STORAGE['API_SECRET']
        )
        
        self.stdout.write("Cloudinary Upload Script")
        self.stdout.write("=" * 60)
        
        # Define upload mappings
        upload_mappings = [
            ('media/products', 'sierra_luxe/products'),
            ('media/landing-page-banner', 'sierra_luxe/landing-page-banner'),
            ('media/categories', 'sierra_luxe/categories'),
            ('media/profiles', 'sierra_luxe/profiles'),
        ]
        
        # Upload each directory
        for source_dir, cloudinary_folder in upload_mappings:
            self.upload_directory(source_dir, cloudinary_folder)
        
        self.stdout.write(self.style.SUCCESS("\nUpload process completed!"))

    def upload_file_to_cloudinary(self, file_path, folder):
        """Upload a single file to Cloudinary"""
        try:
            # Determine resource type based on file extension
            file_ext = file_path.suffix.lower()
            if file_ext in ['.mp4', '.mov', '.avi', '.webm']:
                resource_type = 'video'
            else:
                resource_type = 'image'
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                str(file_path),
                folder=folder,
                resource_type=resource_type,
                public_id=file_path.stem,  # Use filename without extension as public_id
                overwrite=True
            )
            
            self.stdout.write(f"✓ Uploaded: {file_path.name} -> {result['public_id']}")
            return result['secure_url']
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ Failed to upload {file_path.name}: {str(e)}"))
            return None

    def upload_directory(self, source_dir, cloudinary_folder):
        """Upload all files from a directory to Cloudinary"""
        source_path = Path(source_dir)
        if not source_path.exists():
            self.stdout.write(self.style.WARNING(f"Directory not found: {source_dir}"))
            return
        
        files = list(source_path.glob('*'))
        if not files:
            self.stdout.write(self.style.WARNING(f"No files found in: {source_dir}"))
            return
        
        self.stdout.write(f"\nUploading {len(files)} files from {source_dir} to {cloudinary_folder}/")
        self.stdout.write("=" * 60)
        
        success_count = 0
        for file_path in files:
            if file_path.is_file():
                url = self.upload_file_to_cloudinary(file_path, cloudinary_folder)
                if url:
                    success_count += 1
        
        self.stdout.write(f"\nCompleted: {success_count}/{len(files)} files uploaded successfully")
