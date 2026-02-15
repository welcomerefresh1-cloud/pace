#!/bin/bash

# PACE Development - Start All Services
# This script provides easy startup of all development services
# It can either run them in separate terminal tabs or show instructions

echo "🚀 PACE Development - Start All Services"
echo ""

cd "$(dirname "$0")/.." || exit 1

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" &> /dev/null
}

echo "Checking prerequisites..."
echo ""

# Check Docker
if ! command_exists docker; then
    echo "❌ Docker not found"
    DOCKER_OK=0
else
    echo "✅ Docker found"
    DOCKER_OK=1
fi

# Check Node
if ! command_exists node; then
    echo "❌ Node.js not found"
    NODE_OK=0
else
    echo "✅ Node.js found"
    NODE_OK=1
fi

# Check Python
if ! command_exists python3; then
    echo "❌ Python 3 not found"
    PYTHON_OK=0
else
    echo "✅ Python 3 found"
    PYTHON_OK=1
fi

echo ""

# If all requirements are met, try to use a terminal multiplexer
if command_exists tmux; then
    echo "🔧 Using tmux to start all services..."
    echo ""
    
    # Create a new tmux session
    tmux new-session -d -s pace -x 200 -y 50
    
    # Start Docker in window 0
    tmux send-keys -t pace "bash scripts/start-docker.sh" Enter
    tmux rename-window -t pace:0 "Docker"
    
    # Create window 1 for Backend
    tmux new-window -t pace -n "Backend"
    tmux send-keys -t pace:1 "bash scripts/start-backend.sh" Enter
    
    # Create window 2 for Frontend
    tmux new-window -t pace -n "Frontend"
    tmux send-keys -t pace:2 "bash scripts/start-frontend.sh" Enter
    
    # Attach to the session
    echo "✅ All services started in tmux session 'pace'"
    echo ""
    echo "${BLUE}Tmux tips:${NC}"
    echo "  - Switch windows: Ctrl+B then number (0, 1, 2)"
    echo "  - Detach: Ctrl+B then D"
    echo "  - Kill session: tmux kill-session -t pace"
    echo ""
    tmux attach -t pace
    
elif command_exists gnome-terminal; then
    echo "🔧 Using GNOME Terminal to start services..."
    echo ""
    
    gnome-terminal --tab -t "Docker" -- bash scripts/start-docker.sh &
    sleep 2
    gnome-terminal --tab -t "Backend" -- bash scripts/start-backend.sh &
    sleep 2
    gnome-terminal --tab -t "Frontend" -- bash scripts/start-frontend.sh &
    
    echo "✅ Services started in separate terminal tabs"
    
elif command_exists xterm; then
    echo "🔧 Using xterm to start services..."
    echo ""
    
    xterm -T "Docker" -e bash scripts/start-docker.sh &
    xterm -T "Backend" -e bash scripts/start-backend.sh &
    xterm -T "Frontend" -e bash scripts/start-frontend.sh &
    
    echo "✅ Services started in separate xterm windows"
    
else
    echo "📋 Manual startup required (no terminal multiplexer found)"
    echo ""
    echo "Open three separate terminal windows and run:"
    echo ""
    echo -e "${GREEN}Terminal 1 (Docker):${NC}"
    echo "  bash scripts/start-docker.sh"
    echo ""
    echo -e "${GREEN}Terminal 2 (Backend):${NC}"
    echo "  bash scripts/start-backend.sh"
    echo ""
    echo -e "${GREEN}Terminal 3 (Frontend):${NC}"
    echo "  bash scripts/start-frontend.sh"
    echo ""
    echo -e "${YELLOW}Or install tmux for automatic multi-window support:${NC}"
    echo "  Ubuntu/Debian: sudo apt-get install tmux"
    echo "  macOS: brew install tmux"
    echo ""
fi

echo ""
echo -e "${BLUE}Once services are running:${NC}"
echo "  Backend API:    http://localhost:8000"
echo "  API Docs:       http://localhost:8000/docs"
echo "  Frontend:       http://localhost:3000"
echo ""
