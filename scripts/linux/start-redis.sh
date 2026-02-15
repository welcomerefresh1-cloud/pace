#!/bin/bash

# PACE Development - Start Redis Service
# This script starts Redis using Docker Compose

echo "🚀 Starting Redis Service..."
echo ""

# Navigate to project root
cd "$(dirname "$0")/.." || exit 1

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "⏳ Starting Redis container..."
docker-compose up -d redis

echo ""
echo "✅ Redis started successfully"
echo ""
echo "📋 Redis connection string:"
echo "   redis://localhost:6379"
echo ""
echo "🔍 View logs:"
echo "   docker-compose logs -f redis"
echo ""
echo "❌ To stop Redis:"
echo "   bash scripts/stop-redis.sh"
echo ""
