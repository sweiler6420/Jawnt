// src/components/CreateOrganization.js
import React, { useState } from 'react';
import useApi from '../hooks/useApi'
import { useNavigate } from 'react-router-dom';

const CreateOrganization = () => {
    const { apiCreateOrg } = useApi()
    const [orgName, setOrgName] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const navigate = useNavigate();
    
    const handleSubmit = (e) => {
        e.preventDefault();
        let payload = {
            "name": orgName,
            "admin": {
                "first_name": firstName,
                "last_name": lastName,
                "email": email
            }
        }

        apiCreateOrg('organization/', payload).then(
            response => {
                // Redirect to login
                navigate('/login');
            }
        )
    };

    return (
        <div style={{ padding: '1rem' }}>
            <h2 style={{ textAlign: 'center' }}>Create a New Organization</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" placeholder="Organization Name" value={orgName} onChange={(e) => setOrgName(e.target.value)} required/>
                <input type="text" placeholder="First Name" value={firstName} onChange={(e) => setFirstName(e.target.value)} required/>
                <input type="text" placeholder="Last Name" value={lastName} onChange={(e) => setLastName(e.target.value)} required/>
                <input type="text" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required/>
                <button type="submit">Create Organization</button>
            </form>
        </div>
    );
};

export default CreateOrganization;
