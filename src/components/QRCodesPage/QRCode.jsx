/* eslint-disable react/prop-types */
import React from 'react';

export default function QRCodeImage(props) {
  const { qr } = props;

  const file = `data:image/png;base64,${qr.qr_image}`;

  return (
    <div
      className="bg-dark"
      style={{
        width: '200px',
        height: '220px',
        margin: '5px',
        padding: '5px',
      }}
    >
      <div>
        <img src={file} alt={qr.img_name} style={{ width: '190px', height: '190px' }} />
      </div>
      <div className="text-center text-light" style={{ fontSize: '80%' }}>
        {qr.img_name}
      </div>
    </div>
  );
}
