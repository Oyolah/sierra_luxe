#!/bin/bash

# Script to run migrations on production database
echo "Running migrations on production database..."

# Temporarily set DATABASE_URL to production
export DATABASE_URL="postgresql://postgres.drtamonxatronleyvmpc:Sierra_luxe2026@aws-0-eu-west-1.pooler.supabase.com:5432/postgres?sslmode=require"

# Run migrations
python3 manage.py migrate --noinput

# Populate dashboard permissions
echo "Populating dashboard permissions..."
python3 manage.py populate_permissions

echo "Production migrations completed successfully!"
