// src/context/AppContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';

const AppContext = createContext();

export const useAppContext = () => {
  return useContext(AppContext);
};

export const AppProvider = ({ children }) => {
  const [currentUser, setUser] = useState(null);
  const [currentOrganization, setOrganization] = useState(null);
  const [currentInternalAccount, setInternalAccount] = useState(null);
  const [currentExternalAccount, setExternalAccount] = useState(null);
  const [currentDebitCard, setDebitCard] = useState(null);
  const [currentIdempotencyKey, setIdempotencyKey] = useState(null);

  const setCurrentOrganization = (org) => {
    setOrganization(org);
  };

  const setCurrentUser = (user) => {
    setUser(user);
  };

  const setCurrentInternalAccount = (internalAccount) => {
    setInternalAccount(internalAccount)
  }

  const setCurrentExternalAccount = (externalAccount) => {
    setExternalAccount(externalAccount)
  }

  const setCurrentDebitCard = (debitCard) => {
    setDebitCard(debitCard)
  }

  const setCurrentIdempotencyKey = (idempotencyKey) => {
    setIdempotencyKey(idempotencyKey)
  }

  const resetContext = () => {
    setUser(null);
    setOrganization(null);
    setInternalAccount(null);
    setExternalAccount(null);
    setDebitCard(null);
    setIdempotencyKey(null);
  };

  // Log changes to user or organization
  useEffect(() => {
    console.log('currentUser changed:', currentUser);
  }, [currentUser]);

  useEffect(() => {
    console.log('currentOrganization changed:', currentOrganization);
  }, [currentOrganization]);

  useEffect(() => {
    console.log('currentIdempotencyKey changed:', currentIdempotencyKey);
  }, [currentIdempotencyKey]);
  

  return (
    <AppContext.Provider value={{ currentUser, setCurrentUser, 
      currentOrganization, setCurrentOrganization,
      currentInternalAccount, setCurrentInternalAccount,
      currentExternalAccount, setCurrentExternalAccount,
      currentDebitCard, setCurrentDebitCard,
      currentIdempotencyKey, setCurrentIdempotencyKey,
      resetContext
    }}>
      {children}
    </AppContext.Provider>
  );
};
