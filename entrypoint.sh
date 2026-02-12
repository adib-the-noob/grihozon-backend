#!/bin/sh
set -e

echo "Waiting for PostgreSQL to be ready..."

# Wait for PostgreSQL
until python -c "import psycopg2; psycopg2.connect(host='$DB_HOST', port='$DB_PORT', user='$DB_USER', password='$DB_PASSWORD', dbname='$DB_NAME')" 2>/dev/null; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "PostgreSQL is up - executing migrations"

# Run migrations with retry logic
max_attempts=5
attempt=1

while [ $attempt -le $max_attempts ]; do
  echo "Migration attempt $attempt of $max_attempts..."
  
  if python manage.py migrate --noinput; then
    echo "Migrations completed successfully"
    break
  else
    if [ $attempt -eq $max_attempts ]; then
      echo "Migrations failed after $max_attempts attempts"
      exit 1
    fi
    echo "Migration failed, retrying in 3 seconds..."
    sleep 3
    attempt=$((attempt + 1))
  fi
done

# Check if database needs seeding
echo "Checking if database needs seeding..."
PRODUCT_COUNT=$(python -c "
import django
django.setup()
from products.models import Product
print(Product.objects.count())
" 2>/dev/null || echo "0")

if [ "$PRODUCT_COUNT" = "0" ]; then
  echo "No products found - seeding database with sample data..."
  python manage.py seed_products
  echo "Database seeding completed"
else
  echo "Database already has $PRODUCT_COUNT products - skipping seed"
fi

echo "Starting application..."
exec "$@"
