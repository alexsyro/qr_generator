/* eslint-disable react/prop-types */
import React, { useEffect, useState } from 'react';

import Pagination from 'react-bootstrap/Pagination';
import { getQRs } from '../../helpers/helpers';

import QRCodeImage from './QRCode';

export default function QRListComponent(props) {
  const { qrGroup } = props;

  const [currentPage, setCurrentPage] = useState(1);
  const [hasNext, setHasNext] = useState(null);
  const [hasPrev, setHasPrev] = useState(null);
  const [tagsArray, setTagsArray] = useState([]);

  const qrCodesArray = tagsArray.map((prodTag) => (
    <QRCodeImage key={prodTag.img_name} qr={prodTag} />
  ));

  const loadQrs = async () => {
    const data = await getQRs(qrGroup.id, currentPage);
    setTagsArray(data.results);
    if (data.previous) {
      setHasPrev(true);
    } else setHasPrev(false);
    if (data.next) {
      setHasNext(true);
    } else setHasNext(false);
  };

  const onPreviousPageClick = () => {
    if (hasPrev && currentPage > 1) {
      setCurrentPage((prev) => prev - 1);
    }
  };

  const onNextPageClick = () => {
    if (hasNext) {
      setCurrentPage((prev) => prev + 1);
    }
  };

  useEffect(() => {
    if (currentPage) {
      loadQrs();
    }
  }, [currentPage]);

  useEffect(() => {
    if (qrGroup) {
      loadQrs();
    }
    return () => {
      setCurrentPage(1);
      setHasNext(false);
      setHasPrev(false);
      setTagsArray([]);
    };
  }, [qrGroup]);

  return (
    <div>
      <div className="d-flex flex-wrap">
        {qrGroup
          ? qrCodesArray
          : null}
      </div>
      <div className="qrcodes-pagination">
        { tagsArray.length > 0 && (hasNext || hasPrev)
          ? (
            <Pagination>
              <Pagination.Item key="previous" onClick={onPreviousPageClick} disabled={!hasPrev}>
                {'<-'}
              </Pagination.Item>
              <Pagination.Item key={currentPage} active>
                {currentPage}
              </Pagination.Item>
              <Pagination.Item key="next" onClick={onNextPageClick} disabled={!hasNext}>
                {'->'}
              </Pagination.Item>
            </Pagination>
          ) : null}
      </div>
    </div>
  );
}
