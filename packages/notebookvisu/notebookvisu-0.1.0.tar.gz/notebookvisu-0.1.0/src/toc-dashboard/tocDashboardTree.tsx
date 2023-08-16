import React, { useEffect, useState, useRef } from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../redux/store';
import { INotebookModel } from '@jupyterlab/notebook';
import { INotebookHeading } from '../utils/headings';
import {
  TocDashboardItem,
  ConnectedTocDashboardItem
} from './tocDashboardItem';
import { Signal } from '@lumino/signaling';
import { TocDashboardPanel } from './tocDashboardPanel';
import { ItemRenderer } from '../utils/interfaces';
import { ToolbarComponent } from './generator/toolbar_generator';
import { BACKEND_API_URL } from '../utils/constants';
import { areListsEqual, hashCellList } from '../utils/utils';
import { LocationData } from '../redux/types';

interface ITOCTreeProps {
  title: string;
  headings: INotebookHeading[];
  entryClicked?: Signal<TocDashboardPanel, TocDashboardItem>;
  itemRenderer: ItemRenderer;
  Toolbar: ToolbarComponent | null;
  notebookModel: INotebookModel | null;
}

const TocDashboardTree: React.FC<ITOCTreeProps> = props => {
  const notebookCells = useRef<string[] | null | undefined>(null);
  // to abort ongoing API requests
  const fetchToCDataController = useRef<AbortController | undefined>();

  const refreshRequired = useSelector(
    (state: RootState) => state.tocdashboard.refreshBoolean
  );

  const [locationData, setLocationData] = useState<LocationData>(null);

  useEffect(() => {
    const isRefresh: boolean = false;
    fetchToCData(isRefresh);
  }, [props]);

  // useEffect to re-fetch when the refresh button is pressed, should not fetch on the 1st render
  const isInitialRender = useRef(true);
  useEffect(() => {
    if (isInitialRender.current) {
      isInitialRender.current = false;
      return;
    }
    const isRefresh: boolean = true;
    fetchToCData(isRefresh);
  }, [refreshRequired]);

  // useEffect for clean up
  useEffect(() => {
    return () => {
      // clean up callback function when the toc tree will unmount
      if (fetchToCDataController.current) {
        fetchToCDataController.current.abort();
      }
      notebookCells.current = null;
      setLocationData(null);
    };
  }, []);

  const fetchToCData = async (isRefresh: boolean): Promise<void> => {
    const oldCells = notebookCells.current;
    const notebookId = props.notebookModel?.getMetadata('notebook_id');
    updateCellList();

    // only fetch if there is a notebook_id, there are cells
    if (!notebookId || !notebookCells.current) {
      return;
    }

    // (ignore if a refresh) fetch only if the list of cells changed
    if (!isRefresh && areListsEqual(notebookCells.current, oldCells)) {
      return;
    }

    // fetch
    if (fetchToCDataController.current) {
      fetchToCDataController.current.abort();
    }

    try {
      fetchToCDataController.current = new AbortController();
      const signal = fetchToCDataController.current.signal;

      // setLocationData(null);

      const response = await fetch(
        `${BACKEND_API_URL}/dashboard/toc/${notebookId}?hashedList=${hashCellList(
          notebookCells.current
        )}`,
        { signal: signal }
      );

      if (!signal.aborted) {
        if (response.ok) {
          const data = await response.json();
          // process the response data and handle the different scenarios
          if (data.status === 'not_found') {
            // no entry found in the Notebook table for the notebook_id
            console.log('Notebook not registered');
          } else if (data.status === 'hash_mismatch') {
            // hash mismatch between the URL parameter and the notebook table entry
            console.log('Cell list mismatch with the registered notebook');
          } else if (data.status === 'success') {
            console.log('Location data fetched : ', data.data);
            // dispatch(setFetchedLocationData(data.data));
            setLocationData(data.data);
            return;
          }
        } else {
          console.log('Error:', response.status);
        }
      }
    } catch (error) {
      console.log('Error:', error);
    } finally {
      // reset the controller to allow new API calls
      fetchToCDataController.current = undefined;
    }
    // if it didn't fetch, set the fetched data to null
    setLocationData(null);
  };

  const updateCellList = (): void => {
    // const cells = [
    //   { id: 'cell_1_md_JS' },
    //   { id: 'cell_2_md_JS' },
    //   { id: 'cell_3_code_JS' },
    //   { id: 'cell_4_code_JS' },
    //   { id: 'cell_5_code_JS' },
    //   { id: 'cell_6_md_JS' },
    //   { id: 'cell_7_code_JS' },
    //   { id: 'cell_8_code_JS' },
    //   { id: 'cell_9_md' }
    // ];
    const cells = props.notebookModel?.cells;
    if (cells) {
      notebookCells.current = Array.from(cells).map(c => c.id);
    } else {
      notebookCells.current = null;
    }
  };

  return (
    <div className="dashboard-TableOfContents">
      <div className="dashboard-stack-panel-header">{props.title}</div>
      {props.Toolbar && <props.Toolbar />}
      <ul className="dashboard-TableOfContents-content">
        {props.headings.map((el, index) => {
          return (
            <ConnectedTocDashboardItem
              heading={el}
              headings={props.headings}
              entryClicked={props.entryClicked}
              itemRenderer={props.itemRenderer}
              tocDashboardData={
                locationData
                  ? [
                      locationData.location_count[el.cellRef.model.id],
                      locationData.total_count
                    ]
                  : null
              }
              key={`${el.text}-${el.level}-${index++}`}
            />
          );
        })}
      </ul>
    </div>
  );
};

export default TocDashboardTree;
