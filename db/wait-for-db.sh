#!/usr/bin/env sh

host="$1"
port="$2"

echo "Waiting for database to be ready..."
echo "Host: $host"
echo "Port: $port"
echo "DATABASE_URL: $DATABASE_URL"
echo "REWORKD_PLATFORM_DATABASE_URL: $REWORKD_PLATFORM_DATABASE_URL"

until echo "SELECT 1;" | nc "$host" "$port" > /dev/null 2>&1; do
  >&2 echo "Database is unavailable - Sleeping..."

  sleep 2
done

>&2 echo "Database is available! Continuing..."
