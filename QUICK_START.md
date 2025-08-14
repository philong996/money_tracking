# Money Tracker - Quick Setup Guide

## 🚀 Quick Start

### Option 1: Automatic Setup (Recommended)

**For macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

**For Windows:**
```bash
start.bat
```

### Option 2: Manual Setup

**Backend:**
```bash
cd money-tracker-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend (in new terminal):**
```bash
cd money-tracker-frontend
npm install
npm start
```

## 📱 Access Points

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔑 First Steps

1. Register a new account
2. Login with your credentials
3. Add some sample transactions
4. Explore the dashboard and analytics

## 🆘 Need Help?

Check the main README.md for detailed setup instructions and troubleshooting.
