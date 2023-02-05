/* eslint-disable import/no-extraneous-dependencies */
import React from 'react';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { Link } from 'react-router-dom';

export default function NavigationBar() {
  return (
    <Navbar bg="dark" variant="dark">
      <Container>
        <Navbar.Brand>
          QR Generator
        </Navbar.Brand>
        <Nav className="me-auto">
          <Link to="/">
            Create QR group
          </Link>
          <Link to="qrcodes" style={{ marginLeft: '10px' }}>
            List of QR codes
          </Link>
        </Nav>
      </Container>
    </Navbar>
  );
}
