// src/components/CreateOrganization.js
import React, { useState } from 'react';
import { useAppContext } from '../context/AppContext';
import useApi from '../hooks/useApi'

const CreateOrganization = () => {
    const { apiPost } = useApi()
    const { createOrganization, addEmployee } = useAppContext();
    const [orgName, setOrgName] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    
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

        apiPost('organization/organizations', payload).then(
            response => {
                let org = {
                    "name": response.data.name,
                    "uid": response.data.uid,
                    "id": response.data.id,
                }
                createOrganization(org)
                let employee = response.data.administrators[0].employee
                addEmployee(employee)
            }
        )
    };

    return (
        <div>
        <h2>Create a New Organization</h2>
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
