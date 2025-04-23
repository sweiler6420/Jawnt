// src/components/AdminPortal.js
import React, { useEffect, useState } from 'react';
import { useAppContext } from '../context/AppContext';
import useApi from '../hooks/useApi'

const AdminPortal = () => {
    const { currentOrganization } = useAppContext();
    const [employees, setEmployees] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [showEditModal, setShowEditModal] = useState(false);
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const { apiGet, apiPost, apiDelete, apiPut } = useApi();
    const [error, setError] = useState(null);
    const [editingEmployee, setEditingEmployee] = useState(null);

    const fetchEmployees = async () => {
        if (!currentOrganization) {
          setError('Organization not found.');
          return;
        }
    
        try {
          const response = await apiGet(`organization/${currentOrganization.id}/employees`);
          setEmployees(response.data.employees);
        } catch (err) {
          setError('Failed to fetch employees.');
        }
      };
    
    useEffect(() => {
        fetchEmployees();
    }, [currentOrganization]);

    const handleDelete = async (employeeId) => {
        try {
            await apiDelete(`admin/organizations/employees/${employeeId}`);

            // Refetch employees
            fetchEmployees();
        } catch (err) {
            console.error('Error deleting employee:', error);
        }
    };

    const handleAddEmployee = async (e) => {
        e.preventDefault();
        try {
            await apiPost(`admin/organizations/employees`, {
                first_name: firstName,
                last_name: lastName,
                email: email,
            });
            
            // Clear and close
            setFirstName('');
            setLastName('');
            setEmail('');
            setShowModal(false);

            // Refetch employees
            fetchEmployees();
        } catch (err) {
            console.error('Error adding employee:', err);
        }
    };

    const handleEditEmployee = async (e) => {
        e.preventDefault();
        console.log(e)
        try {
            await apiPut(`admin/organizations/employees/${editingEmployee.id}`, {
                first_name: firstName,
                last_name: lastName,
            });
            
            // Clear and close
            setFirstName('');
            setLastName('');
            setEmail('');
            setShowEditModal(false);

            // Refetch employees
            fetchEmployees();
        } catch (err) {
            console.error('Error adding employee:', err);
        }
    };

    const handleCancel = () => {
        setShowModal(false);
        setShowEditModal(false);
        setFirstName('');
        setLastName('');
        setEmail('');
    };

    const openEditModal = (emp) => {
        setEditingEmployee(emp);
        setFirstName(emp.first_name);
        setLastName(emp.last_name);
        setEmail(emp.email);
        setShowEditModal(true);
    };

    // const handleEmployeeSubmit = async (e) => {
    //     e.preventDefault();
      
    //     try {
    //       if (editingEmployee) {
    //         // Update existing employee
    //         await apiPost(`admin/organizations/employees/${editingEmployee.id}`, {
    //           first_name: firstName,
    //           last_name: lastName,
    //           email: email,
    //         });
    //       } else {
    //         // Add new employee
    //         await apiPost(`admin/organizations/employees`, {
    //           first_name: firstName,
    //           last_name: lastName,
    //           email: email,
    //         });
    //       }
      
    //       // Clear and close
    //       setFirstName('');
    //       setLastName('');
    //       setEmail('');
    //       setEditingEmployee(null);
    //       setShowModal(false);
      
    //       fetchEmployees();
    //     } catch (err) {
    //       console.error('Error saving employee:', err);
    //     }
    // };


    return (
        <div style={{ padding: '2rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h2>Admin Portal</h2>
            <button onClick={() => setShowModal(true)}>Add Employee</button>
        </div>

        <table style={{ width: '100%', marginTop: '1rem', borderCollapse: 'collapse' }}>
            <thead>
            <tr style={{ backgroundColor: '#f2f2f2' }}>
                <th style={thStyle}>First Name</th>
                <th style={thStyle}>Last Name</th>
                <th style={thStyle}>Email</th>
                <th style={thStyle}>Actions</th>
            </tr>
            </thead>
            <tbody>
            {employees.map((emp) => (
                <tr key={emp.id}>
                <td style={tdStyle}>{emp.first_name}</td>
                <td style={tdStyle}>{emp.last_name}</td>
                <td style={tdStyle}>{emp.email}</td>
                <td style={tdStyle}>
                    <button onClick={() => handleDelete(emp.id)}>Delete</button>
                    <button style={{ marginLeft: '0.5rem' }} onClick={() => openEditModal(emp)}>Edit</button>
                </td>
                </tr>
            ))}
            </tbody>
        </table>

        {/* Add Modal */}
        {showModal && (
            <div style={modalBackdrop}>
                <div style={modalContent}>
                    <h3>Add Employee</h3>
                    <form onSubmit={handleAddEmployee}>
                        <input type="text" placeholder="First Name" value={firstName} onChange={(e) => setFirstName(e.target.value)} required/>
                        <br />
                        <input type="text" placeholder="Last Name" value={lastName} onChange={(e) => setLastName(e.target.value)} required/>
                        <br />
                        <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required/>
                        <br />
                        <div style={{ marginTop: '1rem' }}>
                            <button type="submit">Submit</button>
                            <button type="button" onClick={handleCancel} style={{ marginLeft: '1rem' }}>
                            Cancel
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        )}

        {/* Edit Modal */}
        {showEditModal && (
            <div style={modalBackdrop}>
                <div style={modalContent}>
                    <h3>Add Employee</h3>
                    <form onSubmit={handleEditEmployee}>
                        <input type="text" placeholder="First Name" value={firstName} onChange={(e) => setFirstName(e.target.value)} required/>
                        <br />
                        <input type="text" placeholder="Last Name" value={lastName} onChange={(e) => setLastName(e.target.value)} required/>
                        <br />
                        <div style={{ marginTop: '1rem' }}>
                            <button type="submit">Submit</button>
                            <button type="button" onClick={handleCancel} style={{ marginLeft: '1rem' }}>
                            Cancel
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        )}
        </div>
    );
};

const thStyle = {
    padding: '10px',
    textAlign: 'left',
    borderBottom: '1px solid #ccc',
};

const tdStyle = {
    padding: '10px',
    borderBottom: '1px solid #eee',
};

const modalBackdrop = {
    position: 'fixed',
    top: 0,
    left: 0,
    width: '100vw',
    height: '100vh',
    backgroundColor: 'rgba(0, 0, 0, 0.4)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000,
};

const modalContent = {
    background: '#fff',
    padding: '2rem',
    borderRadius: '8px',
    width: '300px',
    textAlign: 'center',
};

export default AdminPortal;