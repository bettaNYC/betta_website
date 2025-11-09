#!/bin/bash

echo "🔍 Checking servers..."
echo ""

# Check web server
echo "📡 Web Server (port 8000):"
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "   ✅ Running"
    curl -s http://localhost:8000 > /dev/null && echo "   ✅ Responding" || echo "   ❌ Not responding"
else
    echo "   ❌ Not running"
    echo "   Start with: python3 -m http.server 8000"
fi

echo ""

# Check proxy server
echo "📡 Proxy Server (port 5000):"
if lsof -ti:5000 > /dev/null 2>&1; then
    echo "   ✅ Running"
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/strava/activities?per_page=1)
    if [ "$response" = "200" ]; then
        echo "   ✅ Responding (HTTP $response)"
        data=$(curl -s http://localhost:5000/api/strava/activities?per_page=1)
        if [ "$data" = "[]" ]; then
            echo "   ⚠️  Returning empty array (no runs or API issue)"
        else
            echo "   ✅ Returning data"
        fi
    else
        echo "   ❌ Not responding correctly (HTTP $response)"
    fi
else
    echo "   ❌ Not running"
    echo "   Start with: python3 strava-proxy.py"
fi

echo ""
echo "🌐 Test URLs:"
echo "   Web: http://localhost:8000"
echo "   Runs: http://localhost:8000/running.html"
echo "   Test: http://localhost:8000/test-strava.html"
echo "   Proxy: http://localhost:5000/api/strava/activities?per_page=5"

