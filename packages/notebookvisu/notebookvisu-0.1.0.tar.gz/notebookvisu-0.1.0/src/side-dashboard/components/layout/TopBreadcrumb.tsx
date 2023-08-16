import React from 'react';
import { Stack } from 'react-bootstrap';

import { useSelector } from 'react-redux';
import { RootState } from '../../../redux/store';
import { store, AppDispatch } from '../../../redux/store';
import { navigateToHistory } from '../../../redux/reducers/SideDashboardReducer';

const dispatch = store.dispatch as AppDispatch;

const TopBreadcrumb = (): JSX.Element => {
  const navigationState = useSelector(
    (state: RootState) => state.sidedashboard.navigationState
  );

  return (
    <Stack className="breadcrumb-container" direction="horizontal" gap={2}>
      {navigationState.map((value: any, index: number) => {
        return (
          <div
            className={
              index === navigationState.length - 1
                ? 'breadcrumb-tile-active breadcrumb-tile'
                : 'breadcrumb-tile'
            }
            onClick={() => {
              // only change if actually going to a previous page
              if (index !== navigationState.length - 1) {
                // cut until page of interest since the last page will be loaded
                dispatch(navigateToHistory(index));
              }
            }}
          >
            {value.pageName}
          </div>
        );
      })}
    </Stack>
  );
};

export default TopBreadcrumb;
