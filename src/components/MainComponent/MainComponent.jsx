/* eslint-disable import/no-cycle */
import React, { useContext, useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import { getProductCategories, getProducts, getQRGroups } from '../../helpers/helpers';
import { GlobalContext } from '../App';

import NavigationBar from '../NavigationBar/NavigationBar';
import './MainComponent.css';

export default function MainComponent() {
  const {
    qrGroups, setQrGroups,
    prodCategories, setProdCategories,
    products, setProducts,
  } = useContext(GlobalContext);

  const loadQrGroups = async () => {
    const data = await getQRGroups();
    setQrGroups(data);
  };

  const loadProdCategories = async () => {
    const data = await getProductCategories();
    setProdCategories(data);
  };

  const loadProducts = async () => {
    const data = await getProducts();
    setProducts(data);
  };

  useEffect(() => {
    if (!qrGroups.length) {
      loadQrGroups();
    }
  }, [qrGroups.length]);

  useEffect(() => {
    if (!prodCategories.length) {
      loadProdCategories();
    }
  }, [prodCategories.length]);

  useEffect(() => {
    if (!products.length) {
      loadProducts();
    }
  }, [products.length]);

  return (
    <>
      <NavigationBar />
      <div className="content">
        <Outlet />
      </div>
      <div>Footer</div>
    </>
  );
}
