// src/components/Navbar.js
import React from 'react';
import { useAppContext } from '../context/AppContext';

const Navbar = () => {
  const { setUser, currentUser } = useAppContext();
  
  const handleSwitchUser = () => {
    // Switch between employees or admin
    setUser({
      firstName: 'John',
      lastName: 'Doe',
      email: 'john.doe@example.com'
    });
  };

  return (
    <div>
      <h1>Jawnt</h1>
      <nav>
        <button onClick={() => window.location.href = '/'}>Create Organization</button>
        {currentUser && <button onClick={() => window.location.href = '/employees'}>Employees</button>}
        {currentUser && <button onClick={() => window.location.href = '/payment'}>Payments</button>}
        <button onClick={handleSwitchUser}>
          {currentUser ? `Switch to ${currentUser.firstName}` : 'Login as Employee'}
        </button>
      </nav>
    </div>
  );
};

export default Navbar;
