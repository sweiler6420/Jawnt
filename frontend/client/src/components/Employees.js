// src/components/Employees.js
import React from 'react';
import { useAppContext } from '../context/AppContext';

const Employees = () => {
  const { employees } = useAppContext();

  return (
    <div>
      <h2>Employees</h2>
      <ul>
        {employees.map((emp, index) => (
          <li key={index}>
            {emp.first_name} {emp.last_name} - {emp.email}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Employees;
