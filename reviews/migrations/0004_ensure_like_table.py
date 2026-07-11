# Generated migration to ensure Like table exists in production
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


def ensure_like_table_exists(apps, schema_editor):
    """Create Like table if it doesn't exist"""
    # Try to create the Like model
    Like = apps.get_model('reviews', 'Like')
    try:
        # Check if table exists by trying to query it
        Like.objects.using(schema_editor.connection.alias).count()
    except:
        # Table doesn't exist, create it
        schema_editor.create_model(Like)


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_like'),
    ]

    operations = [
        migrations.RunPython(ensure_like_table_exists, migrations.RunPython.noop),
    ]
