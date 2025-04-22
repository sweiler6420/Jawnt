// src/context/AppContext.js
import React, { createContext, useContext, useState } from 'react';

const AppContext = createContext();

export const useAppContext = () => {
  return useContext(AppContext);
};

export const AppProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [organization, setOrganization] = useState(null);
  const [employees, setEmployees] = useState([]);
  
  const createOrganization = (org) => {
    setOrganization(org);
  };

  const addEmployee = (employee) => {
    setEmployees([...employees, employee]);
  };

  const setUser = (user) => {
    setCurrentUser(user);
  };

  return (
    <AppContext.Provider value={{ currentUser, organization, employees, createOrganization, addEmployee, setUser }}>
      {children}
    </AppContext.Provider>
  );
};
