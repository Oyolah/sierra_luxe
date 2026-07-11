# Raw SQL migration to create Like table if it doesn't exist
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_ensure_like_table'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS reviews_like (
                id BIGSERIAL PRIMARY KEY,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                product_id BIGINT NOT NULL,
                user_id INTEGER NOT NULL,
                UNIQUE(product_id, user_id)
            );
            """,
            reverse_sql="DROP TABLE IF EXISTS reviews_like;"
        ),
    ]
