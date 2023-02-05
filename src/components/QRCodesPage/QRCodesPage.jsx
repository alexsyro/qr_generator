/* eslint-disable import/no-cycle */
import React, { useContext, useEffect, useState } from 'react';

import Badge from 'react-bootstrap/Badge';
import ListGroup from 'react-bootstrap/ListGroup';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';
import Form from 'react-bootstrap/Form';

import { GlobalContext } from '../App';
import QRListComponent from './QRListComponent';
import { createZipLink, deleteZipLink, getZipLinks } from '../../helpers/helpers';

export default function QRCodesPage() {
  const { qrGroups } = useContext(GlobalContext);
  const [qrGroup, setQRGroup] = useState(null);
  const [userEmail, setUserEmail] = useState(null);
  const [zipLinks, setZipLinks] = useState([]);
  const [canCreate, setCanCreate] = useState(false);

  const onQRGroupSelect = (id) => {
    const group = qrGroups.find((g) => g.id === id);
    setQRGroup(group);
  };

  const loadZipLinks = () => {
    getZipLinks(qrGroup.id).then((data) => {
      setZipLinks(data);
    });
  };

  const resetData = () => {
    setZipLinks([]);
    setCanCreate(false);
  };

  const onLinkCreationClick = async () => {
    if (userEmail) {
      if (qrGroup.qr_number >= 50000) {
        alert('Well... I haven\'t worked on optimization. So I think you can watch Harry Potter for now :)');
      }
      setCanCreate(false);
      alert('The operation may take a long time, the link will come to your email. Maybe.');
      await createZipLink(qrGroup.id, userEmail);
      setUserEmail('');
    } else {
      alert('Well, there was supposed to be an email check. And a normal notification. You know, floating. In the corner of the screen, at the top. But it\'s not there.');
    }
  };

  const onLinkDeleteClick = (shortenUrl) => {
    deleteZipLink(shortenUrl);
    setZipLinks((prev) => prev.filter((link) => link.shorten_url !== shortenUrl));
  };

  useEffect(() => {
    if (qrGroup) {
      loadZipLinks();
    }
    return () => resetData();
  }, [qrGroup]);

  useEffect(() => {
    if (qrGroup && zipLinks.length === 0) {
      setCanCreate(true);
    } else {
      setCanCreate(false);
    }
  }, [qrGroup, zipLinks]);

  const listGroupItem = qrGroups.map((group) => (
    <ListGroup.Item
      action
      as="li"
      className="d-flex justify-content-between align-items-start"
      key={`qrgroup-${group.id}`}
      href={`#qrgroup${group.id}`}
      onClick={() => onQRGroupSelect(group.id)}
    >
      <div className="ms-2 me-auto">
        <div className="fw-bold">{group.name}</div>
        {group.product_name}
      </div>
      <Badge bg="primary" pill>
        {group.qr_number}
      </Badge>
    </ListGroup.Item>
  ));

  const zipLinksItem = zipLinks.map((link) => (
    <ListGroup.Item key={link.shorten_url}>
      <div className="d-flex justify-content-between align-items-center">
        <div>
          {new Date(link.created_at).toDateString()}
        </div>
        {link.full_url
          ? <a href={link.full_url} target="_blank" rel="noreferrer">Link</a>
          : 'Creating...'}
        <Button
          variant="outline-dark"
          size="sm"
          hint="Delete"
          onClick={() => onLinkDeleteClick(link.shorten_url)}
        >
          X

        </Button>
      </div>
    </ListGroup.Item>
  ));

  return (
    <Container>
      <Row>
        <Col xs={3}>
          <ListGroup
            className="mb-4"
            style={{
              maxHeight: '400px', overflowY: 'auto',
            }}
          >
            { listGroupItem }
          </ListGroup>
          { qrGroup
            ? (
              <div className="d-grid gap-2">
                { canCreate
                  ? (
                    <>
                      <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                        <Form.Label>Email address</Form.Label>
                        <Form.Control type="email" placeholder="name@example.com" value={userEmail} onChange={(e) => setUserEmail(e.target.value)} />
                      </Form.Group>
                      <Button variant="primary" size="lg" onClick={onLinkCreationClick}>Create and send zip</Button>
                    </>
                  )
                  : (
                    <Alert variant="info">
                      Zip archive is underway. To create a new one, delete the existing ones.
                    </Alert>
                  )}
                <ListGroup variant="flush">{zipLinksItem}</ListGroup>
              </div>
            ) : null}
        </Col>
        <Col xs={9}>
          { qrGroup ? <QRListComponent qrGroup={qrGroup} /> : null }
        </Col>
      </Row>
    </Container>
  );
}
