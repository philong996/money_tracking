# Money Tracker Application

A full-stack money tracking application built with FastAPI (Python) backend and React frontend for educational purposes.

## 🎯 Features

### Priority 1 (Core MVP) ✅
- User registration and login with JWT authentication
- Add, edit, and delete transactions
- Basic categories (Food, Transport, Shopping, Entertainment, Healthcare, Education, Other)
- Dashboard with balance and recent transactions
- Transaction listing and management

### Priority 2 (Enhanced Features) ✅
- Category-based spending analytics with charts
- Monthly summaries and insights
- Responsive design with Tailwind CSS
- Data visualization with pie and bar charts

### Priority 3 (Future Enhancements)
- Export functionality (CSV, PDF)
- Group features for shared expenses
- Advanced reporting and trends
- Dark mode theme

## 📁 Project Structure

```
money_tracking/
├── money-tracker-backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   └── money_tracker.db       # SQLite database (created automatically)
├── money-tracker-frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── contexts/          # React contexts
│   │   ├── App.js
│   │   ├── index.js
│   │   └── styles
│   ├── package.json
│   └── tailwind.config.js
└── README.md
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd money-tracker-backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd money-tracker-frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The application will be available at `http://localhost:3000`

## 🧪 Testing the Application

1. Start both backend and frontend servers
2. Visit `http://localhost:3000`
3. Register a new account
4. Login and explore the features
5. Add some sample transactions to see the analytics

### Sample Test Data
Try adding these transactions to test the application:

**Income:**
- Salary: 20,000,000 VND
- Freelance work: 5,000,000 VND

**Expenses:**
- Groceries: 2,000,000 VND (Food)
- Gas: 800,000 VND (Transport)
- Coffee: 300,000 VND (Food)
- Movie tickets: 400,000 VND (Entertainment)

## 🔧 Technologies Used

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database
- **JWT**: Secure authentication
- **Pydantic**: Data validation using Python type hints

### Frontend
- **React**: JavaScript library for building user interfaces
- **React Router**: Declarative routing for React
- **Axios**: Promise-based HTTP client
- **Recharts**: Composable charting library for React
- **Tailwind CSS**: Utility-first CSS framework

