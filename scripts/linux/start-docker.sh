#!/bin/bash

# PACE Development - Docker Services Manager
# This script manages Redis and other Docker services using docker-compose

echo "🐳 PACE Docker Services Manager"
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

# Parse command line arguments
if [ "$1" == "stop" ]; then
    echo "🛑 Stopping Docker services..."
    docker-compose down
    echo "✅ Docker services stopped"
elif [ "$1" == "restart" ]; then
    echo "🔄 Restarting Docker services..."
    docker-compose down
    docker-compose up -d
    echo "✅ Docker services restarted"
    echo ""
    echo "📍 Redis is running at: redis://localhost:6379"
else
    # Default: start services
    echo "🚀 Starting Docker services..."
    echo ""
    
    # Check if services are already running
    if docker-compose ps | grep -q "Up"; then
        echo "⚠️  Some services are already running. Use './start-docker.sh restart' to restart them."
        echo ""
        docker-compose ps
    else
        docker-compose up -d
        echo ""
        echo "✅ Docker services started in background"
        echo ""
        echo "📍 Redis is running at: redis://localhost:6379"
        echo ""
        echo "Available commands:"
        echo "  ./start-docker.sh stop     - Stop all services"
        echo "  ./start-docker.sh restart  - Restart all services"
        echo ""
        echo "View logs with: docker-compose logs -f [service_name]"
    fi
fi
