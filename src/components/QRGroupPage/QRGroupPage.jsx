/* eslint-disable import/no-cycle */
/* eslint-disable no-shadow */
import React, {
  useContext, useEffect, useRef, useState,
} from 'react';

import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/esm/Container';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';

import { createQRGroup } from '../../helpers/helpers';
import {
  prefixValidator, qRsNumberValidator, suffixValidator, zerosNumberValidator,
} from '../../helpers/validators';
import advtr from '../../assets/advntr.webp';

import { GlobalContext } from '../App';

export default function QRGroupPage() {
  const [category, setCategory] = useState(null);
  const [product, setProduct] = useState(null);
  const [productsList, setProductsList] = useState([]);

  const [groupName, setGroupName] = useState('');
  const [prefix, setPrefix] = useState('');
  const [zerosNumber, setZerosNumber] = useState();
  const [suffix, setSuffix] = useState('');
  const [qrNumber, setQrNumber] = useState(100);
  const [logoFile, setLogoFile] = useState(null);

  const groupNameRef = useRef(null);
  const productRef = useRef(null);
  const prefixRef = useRef(null);
  const zerosNumberRef = useRef(null);
  const suffixRef = useRef(null);
  const qrNumberRef = useRef(null);
  const fileRef = useRef(null);
  const imgRef = useRef(null);

  const { setQrGroups, prodCategories, products } = useContext(GlobalContext);

  const categoriesOptions = prodCategories.map((category) => (
    <option key={`${category.id}${category.name}`}>{ category.name }</option>
  ));

  const productOptions = productsList.map((prod) => (
    <option key={`${prod.id}${prod.name}`}>{ prod.name }</option>
  ));

  const onCategorySelect = (e) => {
    setCategory(e.target.value);
  };

  const onProductSelect = (e) => {
    const prodName = e.target.value;
    const product = productsList.find((prod) => prod.name === prodName);
    setProduct(product);
  };

  const onFileSelect = (e) => {
    const file = e.target.files[0];

    if (!file.type.includes('image')) {
      fileRef.current.classList.add('is-invalid');
      fileRef.current.title = 'Wrong file format';
      setLogoFile();
    } else {
      fileRef.current.classList.remove('is-invalid');
      fileRef.current.title = '';
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        setLogoFile({ file: reader.result, name: file.name });
      };
    }
  };

  const resetData = () => {
    setGroupName('');
    setPrefix('');
    setZerosNumber();
    setSuffix('');
    setQrNumber(100);
    setLogoFile(null);
    setProductsList([]);
    imgRef.current.style.visibility = 'visible';
    setTimeout(() => {
      imgRef.current.style.visibility = 'hidden';
    }, 1000);
  };

  const validateData = () => {
    let isValid = true;
    if (!groupName) {
      groupNameRef.current.classList.add('is-invalid');
      isValid = false;
    } else groupNameRef.current.classList.remove('is-invalid');
    if (!prefixValidator(prefix)) {
      prefixRef.current.classList.add('is-invalid');
      isValid = false;
    } else prefixRef.current.classList.remove('is-invalid');
    if (!suffixValidator(suffix)) {
      suffixRef.current.classList.add('is-invalid');
      isValid = false;
    } else suffixRef.current.classList.remove('is-invalid');
    if (!zerosNumberValidator(zerosNumber)) {
      zerosNumberRef.current.classList.add('is-invalid');
      isValid = false;
    } else zerosNumberRef.current.classList.remove('is-invalid');
    if (!qRsNumberValidator(qrNumber)) {
      qrNumberRef.current.classList.add('is-invalid');
      isValid = false;
    } else qrNumberRef.current.classList.remove('is-invalid');
    if (!product) {
      productRef.current.classList.add('is-invalid');
      isValid = false;
    } else productRef.current.classList.remove('is-invalid');
    return isValid;
  };

  const handlerOnSubmit = (e) => {
    e.preventDefault();
    const isValid = validateData();
    if (isValid) {
      if (Number(qrNumber) >= 100000) {
        alert('Wait a little bit.');
      }
      const data = {
        logo: logoFile,
        name: groupName,
        prefix,
        suffix,
        zeros: zerosNumber,
        qr_number: qrNumber,
        product_id: product.id,
      };
      createQRGroup(data).then((data) => {
        setQrGroups((prev) => prev.push(data));
        alert('QR Group is created');
      });
      resetData();
    }
  };

  useEffect(() => {
    if (category) {
      const currProducts = products.filter((prod) => prod.category_name === category);
      setProductsList(currProducts);
      setProduct(currProducts[0]);
    }
  }, [category]);

  return (
    <Container>
      <Form>
        <Row className="mb-2">
          <Col
            xs={3}
            className="d-flex flex-coulmn justify-content-center align-items-center"
            style={{ backgroundColor: 'black' }}
          >
            <Row className="d-flex flex-coulmn justify-content-center align-items-center">
              <img ref={imgRef} src={advtr} alt="Hi there" style={{ visibility: 'hidden' }} />
              <div className="text-center text-light" style={{ fontSize: '25px', height: '30px' }}>
                {`${prefix} ${zerosNumber > 0 ? '0'.repeat(zerosNumber - 1) : ''}1 ${suffix}`}
              </div>
            </Row>
          </Col>

          <Col xs={4}>
            <Row>
              <Form.Group as={Col} controlId="formGridGroupName">
                <Form.Label className="text-light">Group name</Form.Label>
                <Form.Control ref={groupNameRef} type="text" placeholder="Enter the name" value={groupName} onChange={(e) => setGroupName(e.target.value)} />
              </Form.Group>
            </Row>
            <Row>
              <Form.Group as={Col} controlId="formGridCategories">
                <Form.Label className="text-light">Categories</Form.Label>
                <Form.Select onChange={onCategorySelect}>
                  <option> Choose category </option>
                  { categoriesOptions }
                </Form.Select>
              </Form.Group>

              <Form.Group as={Col} controlId="formGridProducts">
                <Form.Label className="text-light">Products</Form.Label>
                <Form.Select ref={productRef} onChange={onProductSelect}>
                  { productOptions}
                </Form.Select>
              </Form.Group>
            </Row>

            <Row>
              <Form.Group as={Col} controlId="formGridPrefix">
                <Form.Label className="text-light">Prefix</Form.Label>
                <Form.Control ref={prefixRef} placeholder="Enter prefix" maxLength="10" type="prefix" value={prefix.toUpperCase()} onChange={(e) => setPrefix(e.target.value.toUpperCase())} />
              </Form.Group>

              <Form.Group as={Col} controlId="formGridZerosNumber">
                <Form.Label className="text-light">Zeros number</Form.Label>
                <Form.Control ref={zerosNumberRef} placeholder="Zeros number" min="0" max="10" type="number" value={zerosNumber} onChange={(e) => setZerosNumber(e.target.value)} />
              </Form.Group>
            </Row>

            <Row>
              <Form.Group as={Col} controlId="formGridSuffix">
                <Form.Label className="text-light">Suffix</Form.Label>
                <Form.Control ref={suffixRef} placeholder="Enter suffix" maxLength="10" type="text" value={suffix} onChange={(e) => setSuffix(e.target.value)} />
              </Form.Group>

              <Form.Group as={Col} controlId="formGridQRNumber">
                <Form.Label className="text-light">Number</Form.Label>
                <Form.Control ref={qrNumberRef} placeholder="QRs number" min="1" max="1000000" type="number" value={qrNumber} onChange={(e) => setQrNumber(e.target.value)} />
              </Form.Group>
            </Row>
            <Row>
              <Form.Group controlId="formFile">
                <Form.Label className="text-light">Logo</Form.Label>
                <Form.Control ref={fileRef} type="file" onChange={onFileSelect} />
              </Form.Group>
            </Row>

            <Row style={{ marginTop: '10px', padding: '10px' }}>
              <Button variant="primary" type="submit" onClick={handlerOnSubmit}>
                Make trolls collect QR codes.
              </Button>
            </Row>
          </Col>
        </Row>
      </Form>
    </Container>
  );
}
