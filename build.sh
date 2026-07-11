#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run migrations with error handling
echo "Running database migrations..."
python manage.py migrate --noinput
if [ $? -ne 0 ]; then
    echo "Migration failed!"
    exit 1
fi
echo "Migrations completed successfully"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
    echo "Static file collection failed!"
    exit 1
fi
echo "Static files collected successfully"

echo "Build completed successfully"
