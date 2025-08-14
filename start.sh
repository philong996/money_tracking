#!/bin/bash

# Money Tracker Development Startup Script

echo "🚀 Starting Money Tracker Application..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is not installed. Please install Node.js 16+"
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm is not installed. Please install npm"
    exit 1
fi

echo "✅ All prerequisites are installed"

# Start backend
echo ""
echo "🐍 Starting Backend (FastAPI)..."
cd money-tracker-backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if requirements.txt is newer than last install
if [ requirements.txt -nt venv/pyvenv.cfg ] || [ ! -f venv/.deps_installed ]; then
    echo "📥 Installing Python dependencies..."
    pip install -r requirements.txt
    touch venv/.deps_installed
fi

# Start backend in background
echo "🚀 Starting FastAPI server..."
uvicorn main:app --reload &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo ""
echo "⚛️  Starting Frontend (React)..."
cd ../money-tracker-frontend

# Install dependencies if package.json is newer than node_modules
if [ package.json -nt node_modules/.deps_installed ] || [ ! -f node_modules/.deps_installed ]; then
    echo "📥 Installing Node.js dependencies..."
    npm install
    touch node_modules/.deps_installed
fi

echo "🚀 Starting React development server..."
npm start &
FRONTEND_PID=$!

# Display information
echo ""
echo "✅ Money Tracker Application Started Successfully!"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "👋 Goodbye!"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Wait for user to press Ctrl+C
wait
