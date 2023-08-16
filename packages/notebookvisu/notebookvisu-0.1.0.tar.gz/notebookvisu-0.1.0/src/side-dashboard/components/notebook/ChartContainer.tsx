import React, { ReactComponentElement } from 'react';
import { Card } from 'react-bootstrap';
import Loader from '../placeholder/Loader';
import NoData from '../placeholder/NoData';
import { Bar, Scatter, Pie, ChartProps } from 'react-chartjs-2';

type PassedComponentType =
  | ReactComponentElement<typeof Bar, ChartProps>
  | ReactComponentElement<typeof Scatter, ChartProps>
  | ReactComponentElement<typeof Pie, ChartProps>;

const ChartContainer = ({
  isFetching,
  isNotEmpty,
  PassedComponent,
  title,
  noDataText
}: {
  isFetching: boolean;
  isNotEmpty: boolean | number | undefined;
  PassedComponent: PassedComponentType;
  title: string;
  noDataText: string;
}): JSX.Element => {
  return (
    <>
      {isFetching ? (
        <Loader />
      ) : (
        <>
          {isNotEmpty ? (
            <Card className="chart-card">
              <Card.Title className="chart-card-title">{title}</Card.Title>
              <Card.Body className="chart-card-body">
                {PassedComponent}
              </Card.Body>
            </Card>
          ) : (
            <NoData text={noDataText} />
          )}
        </>
      )}
    </>
  );
};

export default ChartContainer;
