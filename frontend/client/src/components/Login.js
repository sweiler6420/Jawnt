// src/pages/Login.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';
import useApi from '../hooks/useApi'

const Login = () => {
    const navigate = useNavigate();
    const { apiLogin } = useApi()
    const { setCurrentOrganization, setCurrentUser } = useAppContext();
    const [orgName, setOrgName] = useState('');
    const [email, setEmail] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    let payload = {
        "organization_name": orgName,
        "email": email
    }

    console.log(payload)

    apiLogin('employee/login', payload).then(
        response => {
            setCurrentUser(response.employee)
            setCurrentOrganization(response.organization)
            // Redirect to login
            navigate('/payments');
        }
    )
  };

  return (
    <div style={{ padding: '1rem' }}>
        <div>
            <h2 style={{ textAlign: 'center' }}>Login</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" placeholder="Organization Name" value={orgName} onChange={(e) => setOrgName(e.target.value)} required/>
                <input type="text" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required/>
                <button type="submit">Login</button>
            </form>
        </div>
    </div>
  );
};

export default Login;