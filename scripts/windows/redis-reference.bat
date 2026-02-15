@echo off
REM PACE Development - Redis Quick Reference (Windows)

cls
echo.
echo 浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔
echo 罒罒  PACE Development - Redis Quick Reference              罒罒
echo 浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔浔
echo.
echo 🚀 START and STOP REDIS
echo ═══════════════════════════════════════════════════════════════
echo.
echo   Start Redis:
echo     scripts\windows\start-redis.bat
echo.
echo   Stop Redis:
echo     scripts\windows\stop-redis.bat
echo.
echo.
echo 🗑️  CLEAR CACHE
echo ═══════════════════════════════════════════════════════════════
echo.
echo   Clear all Redis cache (with confirmation):
echo     scripts\windows\clear-cache.bat
echo.
echo   ⚠️  This clears ALL cache:
echo      - Bulk job cache (all_jobs)
echo      - Query-specific caches
echo      - Recommended jobs cache
echo.
echo   Use when:
echo      - Testing with fresh data
echo      - Jobs should reload from database
echo      - Debugging cache issues
echo.
echo.
echo 📊 CHECK REDIS STATUS
echo ═══════════════════════════════════════════════════════════════
echo.
echo   List all keys:
echo     docker-compose exec redis redis-cli KEYS "*"
echo.
echo   Count keys:
echo     docker-compose exec redis redis-cli DBSIZE
echo.
echo   See specific key:
echo     docker-compose exec redis redis-cli GET all_jobs
echo.
echo   Monitor in real-time:
echo     docker-compose exec redis redis-cli MONITOR
echo.
echo.
echo 🔍 VIEW LOGS
echo ═══════════════════════════════════════════════════════════════
echo.
echo   Redis logs:
echo     docker-compose logs -f redis
echo.
echo   Backend logs (shows cache operations):
echo     Look for: [CACHE HIT], [CACHE MISS], [CACHE SET]
echo.
echo.
echo 📋 REDIS CONNECTION
echo ═══════════════════════════════════════════════════════════════
echo.
echo   Connection string:
echo     redis://localhost:6379
echo.
echo   Redis CLI (interactive):
echo     docker-compose exec redis redis-cli
echo.
echo.
echo   For detailed documentation, see: scripts\README.md
echo.
echo.

pause
