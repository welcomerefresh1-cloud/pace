#!/bin/bash

# PACE Development - Clear Redis Cache
# This script clears all cached data from Redis

echo "🗑️  PACE Cache Clear Tool"
echo ""

# Navigate to project root
cd "$(dirname "$0")/.." || exit 1

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed."
    exit 1
fi

# Check if Redis is running
if ! docker-compose ps redis | grep -q "Up"; then
    echo "⚠️  Redis is not running. Starting Redis..."
    docker-compose up -d redis
    sleep 2
fi

echo "Are you sure you want to clear ALL cache? This is irreversible. (y/N)"
read -r confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "❌ Cache clear cancelled."
    exit 0
fi

echo ""
echo "⏳ Clearing cache..."

# Get count before
count_before=$(docker-compose exec -T redis redis-cli DBSIZE | grep -oE '[0-9]+')
echo "📊 Keys before clear: $count_before"

# Clear the database
docker-compose exec -T redis redis-cli FLUSHDB > /dev/null 2>&1

echo ""
echo "✅ Cache cleared successfully!"
echo ""
echo "📊 Keys after clear: 0"
echo ""
echo "💡 Next steps:"
echo "   - Restart the backend to reload cache on startup"
echo "   - Or let the cache auto-refresh (jobs refresh every 6 hours)"
echo ""
