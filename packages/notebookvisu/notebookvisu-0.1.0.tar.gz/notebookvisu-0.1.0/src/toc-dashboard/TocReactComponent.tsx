import React from 'react';

const computeTransparency = (value: number, total: number): number => {
  const transparency: number = 2 * (value / total) + 0.1;

  return Math.min(1, transparency);
};

const TocReactComponent = ({
  users,
  total_users,
  cellId
}: {
  users: number;
  total_users: number;
  cellId: string;
}): JSX.Element => {
  const getCurrentTime = (): string => {
    return new Date().toISOString().slice(17, 21);
  };

  return (
    <div
      className="dashboard-toc-react-component"
      style={{
        backgroundColor: `rgba(21, 92, 144, ${computeTransparency(
          users,
          total_users
        )})`
      }}
    >
      {getCurrentTime() +
        ' | ' +
        users +
        '/' +
        total_users +
        '\n(' +
        cellId.slice(0, 6) +
        ')'}
    </div>
  );
};

export default TocReactComponent;
