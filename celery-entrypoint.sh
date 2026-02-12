#!/bin/sh
set -e

echo "Waiting for web service to be ready..."

# Wait for web service to be accessible (migrations completed)
max_wait=60
waited=0

until curl -s http://web:8000 > /dev/null 2>&1 || [ $waited -gt $max_wait ]; do
  echo "Web service not ready yet - waiting... ($waited seconds)"
  sleep 2
  waited=$((waited + 2))
done

if [ $waited -gt $max_wait ]; then
  echo "Warning: Web service took too long to become ready, starting celery anyway..."
else
  echo "Web service is ready - starting celery worker"
fi

# Give it one more second to be safe
sleep 1

exec "$@"
