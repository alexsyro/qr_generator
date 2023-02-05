/* eslint-disable import/no-cycle */
/* eslint-disable react/jsx-no-constructed-context-values */
import React, { createContext, useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import MainComponent from './MainComponent/MainComponent';
import QRGroupPage from './QRGroupPage/QRGroupPage';
import QRCodesPage from './QRCodesPage/QRCodesPage';
import './App.css';

export const GlobalContext = createContext(null);

function App() {
  const [qrGroups, setQrGroups] = useState([]);
  const [prodCategories, setProdCategories] = useState([]);
  const [products, setProducts] = useState([]);
  const [notification, setNotification] = useState({});
  return (
    <GlobalContext.Provider value={{
      qrGroups,
      setQrGroups,
      prodCategories,
      setProdCategories,
      products,
      setProducts,
      notification,
      setNotification,
    }}
    >
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<MainComponent />}>
            <Route index element={<QRGroupPage />} />
            <Route path="qrcodes" element={<QRCodesPage />} />
            <Route path="*" element={<div content="No page" />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </GlobalContext.Provider>
  );
}

export default App;
