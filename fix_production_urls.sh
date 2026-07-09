#!/bin/bash

# Script to fix video and image URLs in production database
echo "Fixing production database URLs..."

# Temporarily set DATABASE_URL to production
export DATABASE_URL="postgresql://postgres.drtamonxatronleyvmpc:Sierra_luxe2026@aws-0-eu-west-1.pooler.supabase.com:5432/postgres?sslmode=require"

# Run the fix command
python3 manage.py fix_image_urls

echo "Production URLs fixed successfully!"
