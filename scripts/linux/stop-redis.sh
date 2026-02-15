#!/bin/bash

# PACE Development - Stop Redis Service
# This script stops Redis using Docker Compose

echo "🛑 Stopping Redis Service..."
echo ""

# Navigate to project root
cd "$(dirname "$0")/.." || exit 1

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed."
    exit 1
fi

# Check if Redis container is running
if ! docker-compose ps redis | grep -q "Up"; then
    echo "⚠️  Redis is not running."
    echo ""
    exit 0
fi

echo "⏳ Stopping Redis container..."
docker-compose stop redis

echo ""
echo "✅ Redis stopped successfully"
echo ""
echo "🚀 To start Redis again:"
echo "   bash scripts/start-redis.sh"
echo ""
