export default async function callApi(url, method = 'GET', body = null, headers = null) {
  const response = await fetch(url, {
    method,
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: headers || {
      'Content-Type': 'application/json',
    },
    body: body ? JSON.stringify(body) : null,
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
  });
  if (response.status < 400) {
    const data = await response.json();
    return data;
  }
  const data = await response.json();
  return new Error(data);
}
