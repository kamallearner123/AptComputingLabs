#!/bin/bash
set -e

until nc -z db 5433; do
    echo "Waiting for database to be ready..."
    sleep 1
done

echo "Database is ready!"
exec "$@"
