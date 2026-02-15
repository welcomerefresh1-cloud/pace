# PACE Development Scripts

Quick-start scripts for running the PACE application during development.

## Prerequisites

### All Platforms
- **Git** - For version control
- **Docker Desktop** - For Redis and database services
- **Python 3.8+** - Backend development
- **Node.js 18+** - Frontend development
- **npm** - Node package manager

### Linux Only
- **tmux** (optional but recommended) - For automatic multi-window support
  ```bash
  # Ubuntu/Debian
  sudo apt-get install tmux
  
  # macOS
  brew install tmux
  ```

## Quick Start

### Linux

```bash
# Make scripts executable (first time only)
chmod +x scripts/linux/*.sh

# Start all services at once (recommended)
./scripts/linux/start-all.sh

# Or start individual services
./scripts/linux/start-backend.sh      # Backend (FastAPI on :8000)
./scripts/linux/start-frontend.sh     # Frontend (Next.js on :3000)
./scripts/linux/start-docker.sh       # Docker services (Redis)
```

### Windows

```batch
REM Start all services at once (recommended)
scripts\windows\start-all.bat

REM Or start individual services
scripts\windows\start-backend.bat       REM Backend (FastAPI on :8000)
scripts\windows\start-frontend.bat      REM Frontend (Next.js on :3000)
scripts\windows\start-docker.bat        REM Docker services (Redis)
```

## Individual Scripts

### Backend (FastAPI)

**Linux:**
```bash
./scripts/linux/start-backend.sh
```

**Windows:**
```batch
scripts\windows\start-backend.bat
```

- Starts FastAPI development server with hot reload
- Available at: `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`
- Requires: Python environment, Redis running

### Frontend (Next.js)

**Linux:**
```bash
./scripts/linux/start-frontend.sh
```

**Windows:**
```batch
scripts\windows\start-frontend.bat
```

- Starts Next.js development server with hot reload
- Available at: `http://localhost:3000`
- Auto-compiles on file changes

### Docker Services

**Linux:**
```bash
./scripts/linux/start-docker.sh          # Start all services
./scripts/linux/start-docker.sh stop     # Stop all services
./scripts/linux/start-docker.sh restart  # Restart all services
```

**Windows:**
```batch
scripts\windows\start-docker.bat           REM Start all services
scripts\windows\start-docker.bat stop      REM Stop all services  
scripts\windows\start-docker.bat restart   REM Restart all services
```

- Manages Redis and other containerized services
- Runs in background after startup
- View logs: `docker-compose logs -f [service_name]`

### Redis Management (Utility Scripts)

Quick utilities for Redis-specific operations:

**Linux:**
```bash
./scripts/linux/start-redis.sh           # Start Redis only
./scripts/linux/stop-redis.sh            # Stop Redis only
./scripts/linux/clear-cache.sh           # Clear all Redis cache (with confirmation)
./scripts/linux/redis-reference.sh       # Quick Redis reference
```

**Windows:**
```batch
scripts\windows\start-redis.bat            REM Start Redis only
scripts\windows\stop-redis.bat             REM Stop Redis only
scripts\windows\clear-cache.bat            REM Clear all Redis cache (with confirmation)
scripts\windows\redis-reference.bat        REM Quick Redis reference
```

**Use Cases:**
- `start-redis.sh` - Start Redis without other services
- `stop-redis.sh` - Stop Redis while keeping backend/frontend running
- `clear-cache.sh` - Clear all job cache (20 free cache keys) for fresh data testing

### All Services (Recommended)

**Linux:**
```bash
./scripts/linux/start-all.sh
```

**Windows:**
```batch
scripts\windows\start-all.bat
```

**Linux with tmux:**
- Automatically opens all services in tmux windows
- Switch windows: `Ctrl+B` then press window number (0, 1, 2)
- Detach: `Ctrl+B` then `D`
- Kill session: `tmux kill-session -t pace`

**Linux without tmux:**
- Opens services in separate terminal windows (GNOME Terminal or xterm)
- Install tmux for better experience: `sudo apt-get install tmux`

**Windows:**
- Opens services in separate command prompt windows
- Close windows individually to stop specific services

## Typical Development Workflow

1. **First time setup:**
   ```bash
   # Make scripts executable (Linux only)
   chmod +x scripts/linux/*.sh
   
   # Install project dependencies
   npm install              # Frontend dependencies
   pip install -r backend/requirements.txt  # Backend dependencies
   ```

2. **Start development:**
   ```bash
   # All at once
   ./scripts/linux/start-all.sh          # Linux
   scripts\windows\start-all.bat         # Windows
   
   # Or individually
   ./scripts/linux/start-docker.sh       # Terminal 1: Redis/Database (Linux)
   scripts\windows\start-docker.bat      # Terminal 1: Redis/Database (Windows)
   ./scripts/linux/start-backend.sh      # Terminal 2: Backend API (Linux)
   scripts\windows\start-backend.bat     # Terminal 2: Backend API (Windows)
   ./scripts/linux/start-frontend.sh     # Terminal 3: Frontend UI (Linux)
   scripts\windows\start-frontend.bat    # Terminal 3: Frontend UI (Windows)
   ```

3. **Access the application:**
   - Frontend: `http://localhost:3000`
   - Backend: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`

## Troubleshooting

### "Command not found" (Linux)

Make scripts executable:
```bash
chmod +x scripts/linux/*.sh
```

### Docker connection error

Ensure Docker Desktop is running. On Linux, verify Docker daemon:
```bash
sudo systemctl start docker
```

### Cache issues

If jobs display stale data or you need fresh data for testing:
```bash
# Clear all Redis cache
./scripts/linux/clear-cache.sh          # Linux
scripts\windows\clear-cache.bat         # Windows

# Restart backend to reload cache
./scripts/linux/start-backend.sh        # Linux
scripts\windows\start-backend.bat       # Windows
```

### Port already in use

If port 8000 or 3000 is already in use:

**Linux/macOS:**
```bash
# Find process on port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

**Windows:**
```batch
REM Find process on port 8000
netstat -ano | findstr :8000

REM Kill process
taskkill /PID <PID> /F
```

### Redis connection failed

Ensure Docker services are running:
```bash
# Check status
docker-compose ps

# Start if not running
./scripts/linux/start-docker.sh          # Linux
scripts\windows\start-docker.bat        # Windows
```

### Python/Node not found

Ensure Python 3.8+ and Node 18+ are installed:
```bash
python --version
node --version
```

## Environment Variables

Create a `.env.local` file in the frontend directory for environment variables:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Create a `.env` file in the backend directory for backend configuration.

## Stopping Services

### Linux with tmux
- Detach: `Ctrl+B` then `D`
- Kill all: `tmux kill-session -t pace`

### Linux with separate terminals
Close each terminal window

### Windows
Close each command prompt window

### All Platforms
```bash
# Stop Docker services while keeping others running
./scripts/linux/start-docker.sh stop          # Linux
scripts\windows\start-docker.bat stop        # Windows
```

## Performance Tips

1. **Use SSD** - Develops much faster on solid state drives
2. **Limit Docker resources** - Adjust in Docker Desktop settings
3. **Install tmux** (Linux) - Better than separate terminals
4. **Close unused applications** - Free up system resources
5. **Monitor processes** - Check system load while developing

## Additional Commands

### Backend (inside backend directory)

```bash
# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "migration name"

# Run tests
pytest
```

### Frontend (inside project root)

```bash
# Build for production
npm run build

# Run production build locally
npm run start

# Lint code
npm run lint
```

### Docker

```bash
# View logs
docker-compose logs -f redis

# Execute command in container
docker-compose exec redis redis-cli
```

## File Structure

```
pace/
├── scripts/
│   ├── linux/
│   │   ├── start-all.sh              # Start all services
│   │   ├── start-backend.sh          # Backend only
│   │   ├── start-frontend.sh         # Frontend only
│   │   ├── start-docker.sh           # Docker services
│   │   ├── start-redis.sh            # Redis only
│   │   ├── stop-redis.sh             # Stop Redis
│   │   ├── clear-cache.sh            # Clear Redis cache
│   │   ├── redis-reference.sh        # Quick reference
│   │   └── README.md                 # This file
│   ├── windows/
│   │   ├── start-all.bat             # Start all services
│   │   ├── start-backend.bat         # Backend only
│   │   ├── start-frontend.bat        # Frontend only
│   │   ├── start-docker.bat          # Docker services
│   │   ├── start-redis.bat           # Redis only
│   │   ├── stop-redis.bat            # Stop Redis
│   │   ├── clear-cache.bat           # Clear Redis cache
│   │   └── redis-reference.bat       # Quick reference
│   └── README.md                     # This file
├── backend/                          # FastAPI backend
├── src/                              # Next.js frontend
└── docker-compose.yml                # Docker configuration
```

## Getting Help

For issues with:
- **Backend**: Check `backend/logs/` directory
- **Frontend**: Check browser console (F12)
- **Docker**: Run `docker-compose logs`
- **General**: Check project README.md and documentation

---

**Last Updated:** February 2026 | **PACE Development Team**
