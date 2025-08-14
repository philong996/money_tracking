import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

function Layout({ children }) {
  const { user, logout } = useAuth();
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <h1 className="text-xl font-bold text-gray-800">💰 Money Tracker</h1>
              </div>
              <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                <Link
                  to="/"
                  className={`${
                    isActive('/') ? 'border-blue-500 text-gray-900' : 'border-transparent text-gray-500 hover:text-gray-700'
                  } inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
                >
                  Dashboard
                </Link>
                <Link
                  to="/transactions"
                  className={`${
                    isActive('/transactions') ? 'border-blue-500 text-gray-900' : 'border-transparent text-gray-500 hover:text-gray-700'
                  } inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
                >
                  Transactions
                </Link>
                <Link
                  to="/analytics"
                  className={`${
                    isActive('/analytics') ? 'border-blue-500 text-gray-900' : 'border-transparent text-gray-500 hover:text-gray-700'
                  } inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
                >
                  Analytics
                </Link>
              </div>
            </div>
            <div className="flex items-center">
              <span className="text-gray-700 mr-4">Hello, {user?.username}</span>
              <button
                onClick={logout}
                className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {children}
      </main>
    </div>
  );
}

export default Layout;
