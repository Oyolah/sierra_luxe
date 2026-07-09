# Generated migration to ensure Store table exists in production
from django.db import migrations, models


def ensure_store_table_exists(apps, schema_editor):
    """Create Store table if it doesn't exist"""
    # Try to create the Store model
    Store = apps.get_model('catalog', 'Store')
    try:
        # Check if table exists by trying to query it
        Store.objects.using(schema_editor.connection.alias).count()
    except:
        # Table doesn't exist, create it
        schema_editor.create_model(Store)


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_alter_category_slug_alter_product_video'),
    ]

    operations = [
        migrations.RunPython(ensure_store_table_exists, migrations.RunPython.noop),
    ]
