import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await axios.get('http://localhost:8000/dashboard');
      setDashboardData(response.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center">Loading...</div>;
  }

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND',
    }).format(amount);
  };

  return (
    <div className="px-4 py-6 sm:px-0">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>
      
      {/* Summary Cards */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-3 mb-8">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                  <span className="text-white font-bold">₫</span>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Balance
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {formatCurrency(dashboardData?.balance || 0)}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                  <span className="text-white font-bold">↑</span>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Income
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {formatCurrency(dashboardData?.total_income || 0)}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center">
                  <span className="text-white font-bold">↓</span>
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Expenses
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {formatCurrency(dashboardData?.total_expenses || 0)}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Monthly Summary */}
      <div className="bg-white shadow overflow-hidden sm:rounded-md mb-8">
        <div className="px-4 py-5 sm:px-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            This Month's Summary
          </h3>
        </div>
        <div className="border-t border-gray-200">
          <div className="px-4 py-5 sm:p-6">
            <div className="grid grid-cols-1 gap-5 sm:grid-cols-3">
              <div>
                <dt className="text-sm font-medium text-gray-500">Income</dt>
                <dd className="mt-1 text-3xl font-semibold text-green-600">
                  {formatCurrency(dashboardData?.monthly_summary?.income || 0)}
                </dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Expenses</dt>
                <dd className="mt-1 text-3xl font-semibold text-red-600">
                  {formatCurrency(dashboardData?.monthly_summary?.expenses || 0)}
                </dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Net</dt>
                <dd className={`mt-1 text-3xl font-semibold ${
                  (dashboardData?.monthly_summary?.net || 0) >= 0 ? 'text-green-600' : 'text-red-600'
                }`}>
                  {formatCurrency(dashboardData?.monthly_summary?.net || 0)}
                </dd>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Transactions */}
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <div className="px-4 py-5 sm:px-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Recent Transactions
          </h3>
        </div>
        <ul className="divide-y divide-gray-200">
          {dashboardData?.recent_transactions?.map((transaction) => (
            <li key={transaction.id}>
              <div className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
                      transaction.transaction_type === 'income' ? 'bg-green-100' : 'bg-red-100'
                    }`}>
                      <span className={`font-bold ${
                        transaction.transaction_type === 'income' ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {transaction.transaction_type === 'income' ? '+' : '-'}
                      </span>
                    </div>
                    <div className="ml-4">
                      <div className="text-sm font-medium text-gray-900">
                        {transaction.description}
                      </div>
                      <div className="text-sm text-gray-500">
                        {transaction.category} • {new Date(transaction.date).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                  <div className={`text-sm font-medium ${
                    transaction.transaction_type === 'income' ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {transaction.transaction_type === 'income' ? '+' : '-'}
                    {formatCurrency(Math.abs(transaction.amount))}
                  </div>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Dashboard;
