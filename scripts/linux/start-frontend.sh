#!/bin/bash

# PACE Development - Start Frontend Server
# This script starts the Next.js frontend development server

echo "🚀 Starting PACE Frontend Server..."
echo ""

# Navigate to project root
cd "$(dirname "$0")/.." || exit 1

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

echo ""
echo "✅ Dependencies ready. Starting Next.js dev server..."
echo "📍 Frontend will be available at: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the development server
npm run dev
