// src/components/PaymentsPage.js
import React, { useState, useEffect } from 'react';
import { useAppContext } from '../context/AppContext';
import useApi from '../hooks/useApi';
import usePoll from '../hooks/usePoll';
import axios from 'axios';

const Payments = () => {
  const { currentOrganization, currentInternalAccount, currentExternalAccount, currentDebitCard, currentIdempotencyKey  } = useAppContext();
  const [payments, setPayments] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const { apiGet, apiPost } = useApi();
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [showCardSwipeModal, setShowCardSwipeModal] = useState(false);  // New state for the card swipe modal
  const [paymentDetails, setPaymentDetails] = useState({ amount: '', type: '' });
  const [cardSwipeDetails, setCardSwipeDetails] = useState({ amount: ''});  // Card swipe payment details

  const fetchPayments = async () => {
    try {
      const response = await apiGet(`employee/payments`);
      console.log(response);
      setPayments(response.data);
    } catch (err) {
      console.log('Failed to fetch payments.');
    }
  };

  const fetchTransactions = async () => {
    try {
      const response = await apiGet(`employee/transactions`);
      console.log(response);
      setTransactions(response.data);
    } catch (err) {
      console.log('Failed to fetch transactions.');
    }
  };

  // Call on mount + every 10 seconds
  usePoll(fetchPayments, 10000, { immediate: true });

  // Call on mount + every 10 seconds
  usePoll(fetchTransactions, 10000, { immediate: true });

  // Handle adding a payment
  const handlePaymentSubmit = async () => {
    try {
      let url = ''
      if(paymentDetails.type === "ACH_DEBIT"){
        url = 'employee/process-ach-debit'
      }else{
        url = 'employee/process-ach-credit'
      }
      const response = await apiPost(url,
        {
          "internal_account_id": String(currentInternalAccount.account_id),
          "external_account_id": String(currentExternalAccount.account_id),
          "amount": paymentDetails.amount * 100,
          "idempotency_key": String(currentIdempotencyKey)
        }
      );
      setShowPaymentModal(false); // Close the modal
    } catch (error) {
      console.error('Error submitting payment:', error);
    }
  };

  // Handle card swipe payment submission
  const handleCardSwipeSubmit = async () => {
    try {
      const response = await apiPost('employee/process-swipe',
        {
          "internal_account_id": String(currentInternalAccount.account_id),
          "external_account_id": String(currentExternalAccount.account_id),
          "amount": cardSwipeDetails.amount * 100,
          "idempotency_key": String(currentIdempotencyKey)
        }
      );
      setShowCardSwipeModal(false); // Close the modal
    } catch (error) {
      console.error('Error submitting payment:', error);
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      {/* Payments Table */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Payments</h2>
        <button onClick={() => setShowPaymentModal(true)}>Make Payment</button>
      </div>
      {Array.isArray(payments) && payments.length > 0 ? (
        <table style={{ width: '100%', marginTop: '1rem', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ backgroundColor: '#f2f2f2' }}>
              <th style={thStyle}>Payment ID</th>
              <th style={thStyle}>Type</th>
              <th style={thStyle}>Amount</th>
            </tr>
          </thead>
          <tbody>
            {payments.map((payment) => (
              <tr key={payment.id}>
                <td style={tdStyle}>{payment.id}</td>
                <td style={tdStyle}>{payment.type}</td>
                <td style={tdStyle}>${(payment.amount_cents / 100).toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>) : (
        <p>No payments available.</p>
      )}
      <br></br>
      {/* Transactions Table */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Transactions</h2>
        <button onClick={() => setShowCardSwipeModal(true)}>Make Card Swipe Payment</button> {/* New button for card swipe */}
      </div>
      {Array.isArray(transactions) && transactions.length > 0 ? (
        <table style={{ width: '100%', marginTop: '1rem', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ backgroundColor: '#f2f2f2' }}>
              <th style={thStyle}>Transaction ID</th>
              <th style={thStyle}>Merchant Name</th>
              <th style={thStyle}>Amount</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((transaction) => (
              <tr key={transaction.id}>
                <td style={tdStyle}>{transaction.id}</td>
                <td style={tdStyle}>{transaction.merchant_name}</td>
                <td style={tdStyle}>${(transaction.amount_cents / 100).toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>) : (
        <p>No transactions available.</p>
      )}

      {/* Payment Modal */}
      {showPaymentModal && (
        <div style={modalOverlayStyle}>
          <div style={modalContentStyle}>
            <h3>Payment</h3>
            <input type="text" placeholder="Amount" value={paymentDetails.amount} onChange={(e) => setPaymentDetails({ ...paymentDetails, amount: e.target.value })}/>
            <select value={paymentDetails.type} onChange={(e) => setPaymentDetails({ ...paymentDetails, type: e.target.value }) } style={{ width: '100%', padding: '8px', marginTop: '10px' }}>
              <option value="">Select Type</option>
              <option value="ACH_DEBIT">ACH Debit</option>
              <option value="ACH_CREDIT">ACH Credit</option>
            </select>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '20px' }}>
              <button onClick={() => setShowPaymentModal(false)} style={{ flex: '1', marginRight: '10px' }}>Cancel</button>
              <button onClick={handlePaymentSubmit} style={{ flex: '1' }}>Submit</button>
            </div>
          </div>
        </div>
      )}

      {/* Card Swipe Modal */}
      {showCardSwipeModal && (
        <div style={modalOverlayStyle}>
          <div style={modalContentStyle}>
            <h3>Card Swipe Transaction</h3>
            <input type="text" placeholder="Amount" value={cardSwipeDetails.amount} onChange={(e) => setCardSwipeDetails({ ...cardSwipeDetails, amount: e.target.value })}/>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '20px' }}>
              <button onClick={() => setShowCardSwipeModal(false)} style={{ flex: '1', marginRight: '10px' }}>Cancel</button>
              <button onClick={handleCardSwipeSubmit} style={{ flex: '1' }}>Submit</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Style objects
const thStyle = {
  padding: '10px',
  textAlign: 'left',
  borderBottom: '1px solid #ccc',
};

const tdStyle = {
  padding: '10px',
  borderBottom: '1px solid #eee',
};

const modalOverlayStyle = {
  position: 'fixed',
  top: 0,
  left: 0,
  width: '100%',
  height: '100%',
  backgroundColor: 'rgba(0, 0, 0, 0.5)',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
};

const modalContentStyle = {
  backgroundColor: '#fff',
  padding: '20px',
  borderRadius: '5px',
  width: '300px',
  textAlign: 'center',
};

export default Payments;
