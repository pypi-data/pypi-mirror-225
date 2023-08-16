import React from 'react';
import { Row, Col, Card } from 'react-bootstrap';

const NoData = ({ text }: { text: string }): JSX.Element => {
  return (
    <Card className="no-data-card">
      <Card.Body>
        <Card.Title>{text}</Card.Title>
      </Card.Body>
    </Card>
  );
};

export default NoData;
