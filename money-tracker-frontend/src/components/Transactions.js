import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editingTransaction, setEditingTransaction] = useState(null);
  const [categories, setCategories] = useState([]);
  const [formData, setFormData] = useState({
    amount: '',
    category: '',
    description: '',
    transaction_type: 'expense',
    date: new Date().toISOString().split('T')[0],
  });

  useEffect(() => {
    fetchTransactions();
    fetchCategories();
  }, []);

  const fetchTransactions = async () => {
    try {
      const response = await axios.get('http://localhost:8000/transactions');
      setTransactions(response.data);
    } catch (error) {
      console.error('Error fetching transactions:', error);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await axios.get('http://localhost:8000/categories');
      setCategories(response.data.categories);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const transactionData = {
        ...formData,
        amount: parseFloat(formData.amount),
        date: new Date(formData.date).toISOString(),
      };

      if (editingTransaction) {
        await axios.put(`http://localhost:8000/transactions/${editingTransaction.id}`, transactionData);
        setEditingTransaction(null);
      } else {
        await axios.post('http://localhost:8000/transactions', transactionData);
      }

      setFormData({
        amount: '',
        category: '',
        description: '',
        transaction_type: 'expense',
        date: new Date().toISOString().split('T')[0],
      });
      setShowForm(false);
      fetchTransactions();
    } catch (error) {
      console.error('Error saving transaction:', error);
    }
  };

  const handleEdit = (transaction) => {
    setEditingTransaction(transaction);
    setFormData({
      amount: transaction.amount.toString(),
      category: transaction.category,
      description: transaction.description,
      transaction_type: transaction.transaction_type,
      date: new Date(transaction.date).toISOString().split('T')[0],
    });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this transaction?')) {
      try {
        await axios.delete(`http://localhost:8000/transactions/${id}`);
        fetchTransactions();
      } catch (error) {
        console.error('Error deleting transaction:', error);
      }
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND',
    }).format(amount);
  };

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Transactions</h1>
        <button
          onClick={() => setShowForm(true)}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Add Transaction
        </button>
      </div>

      {/* Transaction Form Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                {editingTransaction ? 'Edit Transaction' : 'Add New Transaction'}
              </h3>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Amount</label>
                  <input
                    type="number"
                    step="0.01"
                    required
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                    value={formData.amount}
                    onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Category</label>
                  <select
                    required
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  >
                    <option value="">Select Category</option>
                    {categories.map((category) => (
                      <option key={category} value={category}>
                        {category}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Description</label>
                  <input
                    type="text"
                    required
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Type</label>
                  <select
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                    value={formData.transaction_type}
                    onChange={(e) => setFormData({ ...formData, transaction_type: e.target.value })}
                  >
                    <option value="expense">Expense</option>
                    <option value="income">Income</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Date</label>
                  <input
                    type="date"
                    required
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                    value={formData.date}
                    onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                  />
                </div>
                <div className="flex justify-end space-x-3 pt-4">
                  <button
                    type="button"
                    onClick={() => {
                      setShowForm(false);
                      setEditingTransaction(null);
                      setFormData({
                        amount: '',
                        category: '',
                        description: '',
                        transaction_type: 'expense',
                        date: new Date().toISOString().split('T')[0],
                      });
                    }}
                    className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                  >
                    {editingTransaction ? 'Update' : 'Add'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Transactions List */}
      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {transactions.map((transaction) => (
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
                  <div className="flex items-center space-x-4">
                    <div className={`text-sm font-medium ${
                      transaction.transaction_type === 'income' ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {transaction.transaction_type === 'income' ? '+' : '-'}
                      {formatCurrency(Math.abs(transaction.amount))}
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleEdit(transaction)}
                        className="text-blue-600 hover:text-blue-900 text-sm"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(transaction.id)}
                        className="text-red-600 hover:text-red-900 text-sm"
                      >
                        Delete
                      </button>
                    </div>
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

export default Transactions;
