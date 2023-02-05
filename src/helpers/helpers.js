import callApi from './callApi';

export async function getQRGroups() {
  const url = 'http://127.0.0.1:8000/api/qrs/qr_groups/';
  const data = await callApi(url);
  return data;
}

export async function createQRGroup(body) {
  const url = 'http://127.0.0.1:8000/api/qrs/qr_groups/';
  const headers = { 'Content-Type': 'application/json' };
  const data = await callApi(url, 'POST', body, headers);
  return data;
}

export async function getProductCategories() {
  const url = 'http://127.0.0.1:8000/api/products/categories/';
  const data = await callApi(url);
  return data;
}

export async function getProducts() {
  const url = 'http://127.0.0.1:8000/api/products/';
  const data = await callApi(url);
  return data;
}

export async function getZipLinks(groupId) {
  const url = `http://127.0.0.1:8000/api/qrs/zips/?qrgroupid=${groupId}`;
  const data = await callApi(url);
  return data;
}

export async function deleteZipLink(shortenUrl) {
  const url = `http://127.0.0.1:8000/api/qrs/zips/${shortenUrl}/`;
  const data = await callApi(url, 'DELETE');
  return data;
}

export async function getQRs(groupId, page) {
  const url = `http://127.0.0.1:8000/api/qrs/tags/?qrgroupid=${groupId}&page=${page}`;
  const data = await callApi(url);
  return data;
}

export async function createZipLink(groupId, email) {
  const url = `http://127.0.0.1:8000/api/qrs/zips/?qrgroupid=${groupId}&email=${email}`;
  const data = await callApi(url, 'POST');
  return data;
}
