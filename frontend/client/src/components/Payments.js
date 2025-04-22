// src/components/Payment.js
import React, { useState } from 'react';
import { useAppContext } from '../context/AppContext';

const Payment = () => {
  const { currentUser } = useAppContext();
  const [amount, setAmount] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (currentUser) {
      // Submit the payment
      console.log(`Payment of ${amount} submitted by ${currentUser.firstName}`);
    } else {
      alert('Please log in to submit a payment');
    }
  };

  return (
    <div>
      <h2>Submit Payment</h2>
      <form onSubmit={handleSubmit}>
        <input 
          type="number" 
          placeholder="Amount" 
          value={amount}
          onChange={(e) => setAmount(e.target.value)} 
          required
        />
        <button type="submit">Submit Payment</button>
      </form>
    </div>
  );
};

export default Payment;
