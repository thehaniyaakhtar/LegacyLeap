#!/bin/bash

echo "Starting AS/400 Legacy Modernization Assistant..."
echo

echo "[1/3] Starting Backend Server..."
cd backend
python main.py &
BACKEND_PID=$!
sleep 3

echo "[2/3] Starting Frontend Server..."
cd ../my-legacy-modernizer
npm run dev &
FRONTEND_PID=$!
sleep 3

echo "[3/3] Opening Browser..."
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:3000
elif command -v open > /dev/null; then
    open http://localhost:3000
fi

echo
echo "✅ System started successfully!"
echo
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo
echo "Press Ctrl+C to stop all services..."

# Function to cleanup on exit
cleanup() {
    echo
    echo "Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit
}

# Trap Ctrl+C
trap cleanup INT

# Wait for user to stop
wait
