# Generated migration to ensure RecentlyViewed table exists in production
from django.db import migrations


def ensure_recentlyviewed_table_exists(apps, schema_editor):
    """Create RecentlyViewed table if it doesn't exist"""
    # Try to create the RecentlyViewed model
    RecentlyViewed = apps.get_model('users', 'RecentlyViewed')
    try:
        # Check if table exists by trying to query it
        RecentlyViewed.objects.using(schema_editor.connection.alias).count()
    except:
        # Table doesn't exist, create it
        schema_editor.create_model(RecentlyViewed)


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_recentlyviewed'),
    ]

    operations = [
        migrations.RunPython(ensure_recentlyviewed_table_exists, migrations.RunPython.noop),
    ]
