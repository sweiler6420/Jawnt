// src/App.js
import React from 'react';
import { AppProvider, useAppContext } from './context/AppContext';
import CreateOrganization from './components/CreateOrganization';
import Employees from './components/Employees';
import Payment from './components/Payments';
import Navbar from './components/Navbar';

const App = () => {
  const { organization } = useAppContext();

  console.log(organization)

  return (
    <div>
      <Navbar />
      <div style={{ padding: '20px' }}>
        {/* Show active organization scope */}
        {organization && (
          <div
            style={{
              backgroundColor: '#e3f2fd',
              padding: '10px 20px',
              marginBottom: '20px',
              borderRadius: '6px',
              border: '1px solid #90caf9',
              fontWeight: 'bold',
              color: '#0d47a1',
            }}
          >
            Active Organization: {organization.name}
          </div>
        )}

        {/* Show CreateOrganization if no org yet, otherwise show Employees and Payments */}
        {!organization && <CreateOrganization />}
        {organization && <Employees />}
        {organization && <Payment />}
      </div>
    </div>
  );
};

const AppWrapper = () => (
  <AppProvider>
    <App />
  </AppProvider>
);

export default AppWrapper;
