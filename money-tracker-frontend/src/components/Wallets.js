import React, { useState, useEffect } from 'react';
import './Wallets.css';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

const walletIcons = {
  wallet: '💳',
  cash: '💵',
  bank_account: '🏦',
  credit_card: '💳',
  savings: '🏛️',
  investment: '📈',
  digital_wallet: '📱'
};

const walletTypes = [
  { value: 'cash', label: 'Cash' },
  { value: 'bank_account', label: 'Bank Account' },
  { value: 'credit_card', label: 'Credit Card' },
  { value: 'savings', label: 'Savings' },
  { value: 'investment', label: 'Investment' },
  { value: 'digital_wallet', label: 'Digital Wallet' }
];

const defaultColors = [
  '#4F46E5', '#7C3AED', '#DC2626', '#EA580C', '#D97706',
  '#CA8A04', '#65A30D', '#16A34A', '#059669', '#0891B2',
  '#0284C7', '#2563EB', '#4338CA', '#7C2D12', '#A21CAF'
];

function Wallets() {
  const [wallets, setWallets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingWallet, setEditingWallet] = useState(null);
  const [showTransferForm, setShowTransferForm] = useState(false);
  const [selectedWallet, setSelectedWallet] = useState(null);
  const [error, setError] = useState('');

  const [newWallet, setNewWallet] = useState({
    name: '',
    wallet_type: 'cash',
    icon: 'wallet',
    color: '#4F46E5',
    initial_balance: 0,
    description: '',
    is_default: false
  });

  const [transferData, setTransferData] = useState({
    from_wallet_id: '',
    to_wallet_id: '',
    amount: '',
    description: ''
  });

  const [balanceAdjustment, setBalanceAdjustment] = useState({
    new_balance: '',
    reason: ''
  });

  useEffect(() => {
    fetchWallets();
  }, []);

  const fetchWallets = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/wallets`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setWallets(data);
      } else {
        setError('Failed to fetch wallets');
      }
    } catch (error) {
      setError('Error fetching wallets');
    } finally {
      setLoading(false);
    }
  };

  const createWallet = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/wallets`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newWallet),
      });

      if (response.ok) {
        fetchWallets();
        setShowAddForm(false);
        setNewWallet({
          name: '',
          wallet_type: 'cash',
          icon: 'wallet',
          color: '#4F46E5',
          initial_balance: 0,
          description: '',
          is_default: false
        });
      } else {
        setError('Failed to create wallet');
      }
    } catch (error) {
      setError('Error creating wallet');
    }
  };

  const updateWallet = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/wallets/${editingWallet.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(editingWallet),
      });

      if (response.ok) {
        fetchWallets();
        setEditingWallet(null);
      } else {
        setError('Failed to update wallet');
      }
    } catch (error) {
      setError('Error updating wallet');
    }
  };

  const deleteWallet = async (walletId) => {
    if (!window.confirm('Are you sure you want to delete this wallet?')) return;

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/wallets/${walletId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        fetchWallets();
      } else {
        setError('Failed to delete wallet');
      }
    } catch (error) {
      setError('Error deleting wallet');
    }
  };

  const transferMoney = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/wallets/transfer`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...transferData,
          amount: parseFloat(transferData.amount)
        }),
      });

      if (response.ok) {
        fetchWallets();
        setShowTransferForm(false);
        setTransferData({
          from_wallet_id: '',
          to_wallet_id: '',
          amount: '',
          description: ''
        });
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to transfer money');
      }
    } catch (error) {
      setError('Error transferring money');
    }
  };

  const adjustBalance = async (walletId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/wallets/${walletId}/adjust`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          wallet_id: walletId,
          new_balance: parseFloat(balanceAdjustment.new_balance),
          reason: balanceAdjustment.reason
        }),
      });

      if (response.ok) {
        fetchWallets();
        setSelectedWallet(null);
        setBalanceAdjustment({ new_balance: '', reason: '' });
      } else {
        setError('Failed to adjust balance');
      }
    } catch (error) {
      setError('Error adjusting balance');
    }
  };

  if (loading) return <div className="loading">Loading wallets...</div>;

  return (
    <div className="wallets-container">
      <div className="wallets-header">
        <h1>My Wallets</h1>
        <div className="wallets-actions">
          <button 
            className="btn btn-primary"
            onClick={() => setShowAddForm(true)}
          >
            Add New Wallet
          </button>
          <button 
            className="btn btn-secondary"
            onClick={() => setShowTransferForm(true)}
          >
            Transfer Money
          </button>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="wallets-grid">
        {wallets.map(wallet => (
          <div key={wallet.id} className="wallet-card" style={{ borderColor: wallet.color }}>
            <div className="wallet-header">
              <div className="wallet-icon" style={{ backgroundColor: wallet.color }}>
                {walletIcons[wallet.icon] || '💳'}
              </div>
              <div className="wallet-info">
                <h3>{wallet.name}</h3>
                <span className="wallet-type">
                  {walletTypes.find(t => t.value === wallet.wallet_type)?.label}
                </span>
                {wallet.is_default && <span className="default-badge">Default</span>}
              </div>
            </div>
            
            <div className="wallet-balance">
              <span className="balance-label">Balance</span>
              <span className="balance-amount">${wallet.balance.toFixed(2)}</span>
            </div>

            {wallet.description && (
              <div className="wallet-description">{wallet.description}</div>
            )}

            <div className="wallet-actions">
              <button 
                className="btn btn-sm btn-outline"
                onClick={() => setEditingWallet(wallet)}
              >
                Edit
              </button>
              <button 
                className="btn btn-sm btn-outline"
                onClick={() => {
                  setSelectedWallet(wallet);
                  setBalanceAdjustment({ ...balanceAdjustment, new_balance: wallet.balance });
                }}
              >
                Adjust
              </button>
              <button 
                className="btn btn-sm btn-danger"
                onClick={() => deleteWallet(wallet.id)}
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Add Wallet Modal */}
      {showAddForm && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h2>Add New Wallet</h2>
              <button 
                className="close-btn"
                onClick={() => setShowAddForm(false)}
              >
                ×
              </button>
            </div>
            <form onSubmit={createWallet}>
              <div className="form-group">
                <label>Wallet Name</label>
                <input
                  type="text"
                  value={newWallet.name}
                  onChange={(e) => setNewWallet({ ...newWallet, name: e.target.value })}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Wallet Type</label>
                <select
                  value={newWallet.wallet_type}
                  onChange={(e) => setNewWallet({ ...newWallet, wallet_type: e.target.value })}
                >
                  {walletTypes.map(type => (
                    <option key={type.value} value={type.value}>{type.label}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Color</label>
                <div className="color-picker">
                  {defaultColors.map(color => (
                    <div
                      key={color}
                      className={`color-option ${newWallet.color === color ? 'selected' : ''}`}
                      style={{ backgroundColor: color }}
                      onClick={() => setNewWallet({ ...newWallet, color })}
                    />
                  ))}
                </div>
              </div>

              <div className="form-group">
                <label>Initial Balance</label>
                <input
                  type="number"
                  step="0.01"
                  value={newWallet.initial_balance}
                  onChange={(e) => setNewWallet({ ...newWallet, initial_balance: parseFloat(e.target.value) || 0 })}
                />
              </div>

              <div className="form-group">
                <label>Description (Optional)</label>
                <textarea
                  value={newWallet.description}
                  onChange={(e) => setNewWallet({ ...newWallet, description: e.target.value })}
                />
              </div>

              <div className="form-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={newWallet.is_default}
                    onChange={(e) => setNewWallet({ ...newWallet, is_default: e.target.checked })}
                  />
                  Set as default wallet
                </label>
              </div>

              <div className="modal-actions">
                <button type="button" onClick={() => setShowAddForm(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary">Create Wallet</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit Wallet Modal */}
      {editingWallet && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h2>Edit Wallet</h2>
              <button 
                className="close-btn"
                onClick={() => setEditingWallet(null)}
              >
                ×
              </button>
            </div>
            <form onSubmit={updateWallet}>
              <div className="form-group">
                <label>Wallet Name</label>
                <input
                  type="text"
                  value={editingWallet.name}
                  onChange={(e) => setEditingWallet({ ...editingWallet, name: e.target.value })}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Wallet Type</label>
                <select
                  value={editingWallet.wallet_type}
                  onChange={(e) => setEditingWallet({ ...editingWallet, wallet_type: e.target.value })}
                >
                  {walletTypes.map(type => (
                    <option key={type.value} value={type.value}>{type.label}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Color</label>
                <div className="color-picker">
                  {defaultColors.map(color => (
                    <div
                      key={color}
                      className={`color-option ${editingWallet.color === color ? 'selected' : ''}`}
                      style={{ backgroundColor: color }}
                      onClick={() => setEditingWallet({ ...editingWallet, color })}
                    />
                  ))}
                </div>
              </div>

              <div className="form-group">
                <label>Description</label>
                <textarea
                  value={editingWallet.description || ''}
                  onChange={(e) => setEditingWallet({ ...editingWallet, description: e.target.value })}
                />
              </div>

              <div className="form-group">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={editingWallet.is_default}
                    onChange={(e) => setEditingWallet({ ...editingWallet, is_default: e.target.checked })}
                  />
                  Set as default wallet
                </label>
              </div>

              <div className="modal-actions">
                <button type="button" onClick={() => setEditingWallet(null)}>Cancel</button>
                <button type="submit" className="btn btn-primary">Update Wallet</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Transfer Money Modal */}
      {showTransferForm && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h2>Transfer Money</h2>
              <button 
                className="close-btn"
                onClick={() => setShowTransferForm(false)}
              >
                ×
              </button>
            </div>
            <form onSubmit={transferMoney}>
              <div className="form-group">
                <label>From Wallet</label>
                <select
                  value={transferData.from_wallet_id}
                  onChange={(e) => setTransferData({ ...transferData, from_wallet_id: e.target.value })}
                  required
                >
                  <option value="">Select source wallet</option>
                  {wallets.map(wallet => (
                    <option key={wallet.id} value={wallet.id}>
                      {wallet.name} (${wallet.balance.toFixed(2)})
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>To Wallet</label>
                <select
                  value={transferData.to_wallet_id}
                  onChange={(e) => setTransferData({ ...transferData, to_wallet_id: e.target.value })}
                  required
                >
                  <option value="">Select destination wallet</option>
                  {wallets
                    .filter(wallet => wallet.id.toString() !== transferData.from_wallet_id)
                    .map(wallet => (
                      <option key={wallet.id} value={wallet.id}>
                        {wallet.name}
                      </option>
                    ))}
                </select>
              </div>

              <div className="form-group">
                <label>Amount</label>
                <input
                  type="number"
                  step="0.01"
                  value={transferData.amount}
                  onChange={(e) => setTransferData({ ...transferData, amount: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label>Description (Optional)</label>
                <input
                  type="text"
                  value={transferData.description}
                  onChange={(e) => setTransferData({ ...transferData, description: e.target.value })}
                />
              </div>

              <div className="modal-actions">
                <button type="button" onClick={() => setShowTransferForm(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary">Transfer</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Balance Adjustment Modal */}
      {selectedWallet && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h2>Adjust Balance - {selectedWallet.name}</h2>
              <button 
                className="close-btn"
                onClick={() => setSelectedWallet(null)}
              >
                ×
              </button>
            </div>
            <div className="current-balance">
              Current Balance: ${selectedWallet.balance.toFixed(2)}
            </div>
            <form onSubmit={(e) => { e.preventDefault(); adjustBalance(selectedWallet.id); }}>
              <div className="form-group">
                <label>New Balance</label>
                <input
                  type="number"
                  step="0.01"
                  value={balanceAdjustment.new_balance}
                  onChange={(e) => setBalanceAdjustment({ ...balanceAdjustment, new_balance: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label>Reason for Adjustment</label>
                <textarea
                  value={balanceAdjustment.reason}
                  onChange={(e) => setBalanceAdjustment({ ...balanceAdjustment, reason: e.target.value })}
                  placeholder="e.g., Bank reconciliation, cash count correction..."
                />
              </div>

              <div className="modal-actions">
                <button type="button" onClick={() => setSelectedWallet(null)}>Cancel</button>
                <button type="submit" className="btn btn-primary">Adjust Balance</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default Wallets;
