// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import CreateOrganization from './components/CreateOrganization';
import Login from './components/Login';
import Payments from './components/Payments';
import AdminPortal from './components/AdminPortal';
import AppInitializer from './components/AppInitializer'; // Import the AppInitializer

const App = () => {
  return (
    <>
      <AppInitializer />
      <Navbar />
      <Routes>
        <Route path="/" element={<CreateOrganization />} />
        <Route path="/login" element={<Login />} />
        <Route path="/payments" element={<Payments />} />
        <Route path="/admin" element={<AdminPortal />} />
      </Routes>
    </>
  );
};

export default App;