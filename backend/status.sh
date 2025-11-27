#!/usr/bin/env bash

# Moi AIMER Toi - Backend Status Dashboard
# Run this script to see the status of your backend and frontend servers

echo "🎯 Moi AIMER Toi - Backend Status Dashboard"
echo "==========================================="
echo ""

# Check Frontend
echo "🌐 Frontend Server (http://localhost:8000)"
if curl -s http://localhost:8000 > /dev/null 2>&1; then
    echo "   ✅ Status: RUNNING"
else
    echo "   ❌ Status: NOT RUNNING"
    echo "   💡 Start with: python3 -m http.server 8000"
fi

echo ""

# Check Backend
echo "⚙️  Backend API Server (http://localhost:3001)"
if curl -s http://localhost:3001/api/health > /dev/null 2>&1; then
    echo "   ✅ Status: RUNNING"
    HEALTH=$(curl -s http://localhost:3001/api/health)
    echo "   📡 Response: $HEALTH"
else
    echo "   ❌ Status: NOT RUNNING"
    echo "   💡 Start with: python3 /Users/apple/Moi-aimer-toi/Moi-AIMER-Toi/backend/app.py"
fi

echo ""

# Check Database
DB_PATH="/Users/apple/Moi-aimer-toi/Moi-AIMER-Toi/backend/moi_aimer_toi.db"
if [ -f "$DB_PATH" ]; then
    DB_SIZE=$(du -h "$DB_PATH" | cut -f1)
    echo "💾 Database (SQLite)"
    echo "   ✅ Exists: $DB_PATH"
    echo "   📊 Size: $DB_SIZE"
else
    echo "💾 Database (SQLite)"
    echo "   ⏳ Will be created on first backend start"
fi

echo ""
echo "==========================================="
echo "📚 Documentation"
echo "   📖 API Reference: backend/README.md"
echo "   🔗 Integration Guide: backend/INTEGRATION_GUIDE.md"
echo "   🚀 Quick Start: BACKEND_QUICKSTART.md"
echo ""
echo "🔗 Quick Links"
echo "   Frontend: http://localhost:8000"
echo "   Backend API: http://localhost:3001"
echo "   API Docs: http://localhost:3001/api/health"
