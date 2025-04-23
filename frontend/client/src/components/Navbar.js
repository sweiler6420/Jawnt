// src/components/Navbar.js
import React from 'react';
import { useNavigate, useLocation  } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const {currentUser, currentOrganization, resetContext} = useAppContext();

  const handleLogout = () => {
    resetContext()
    navigate('/login');
  };

  return (
    <>
      <div style={{ backgroundColor: '#333', color: '#fff', padding: '0.5rem 0', textAlign: 'center', fontSize: '1.5rem', fontWeight: 'bold' }}>
        Org Portal
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem', backgroundColor: '#f5f5f5' }}>
        <div style={{ display: 'flex', gap: '1rem' }}>
          {!currentUser && !currentOrganization && location.pathname !== '/' && (
            <button onClick={() => navigate('/')}>Create Organization</button>
          )}
          {currentUser && <button onClick={() => navigate('/payments')}>Payments</button>}
          {currentUser?.is_admin && <button onClick={() => navigate('/admin')}>Admin Portal</button>}
        </div>
        <div>
          {!currentUser && location.pathname !== '/login' ? (
            <button onClick={() => navigate('/login')}>Login</button>
            ) : (
            currentUser && <button onClick={handleLogout}>Logout</button>
          )}
        </div>
      </div>
    </>
  );
};

export default Navbar;