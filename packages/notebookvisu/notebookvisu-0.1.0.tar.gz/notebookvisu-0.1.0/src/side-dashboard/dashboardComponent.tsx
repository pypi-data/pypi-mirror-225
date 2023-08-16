import React, { useEffect, useState, useRef } from 'react';
import { NotebookPanel } from '@jupyterlab/notebook';
import NoNotebookPlaceholder from '../toc-dashboard/NoNotebookPlaceholder';
import { Provider } from 'react-redux';
import PageRouter from './PageRouter';
import { store } from '../redux/store';
import InvalidNotebookPlaceholder from './InvalidNotebookPlaceholder';
import { BACKEND_API_URL } from '../utils/constants';
import { hashCellList } from '../utils/utils';
import Loader from './components/placeholder/Loader';

const DashboardComponent = (props: {
  panel: NotebookPanel | null;
  cellIds: string[] | null;
}): JSX.Element => {
  const [isChecking, setIsChecking] = useState<boolean>(true);
  const [isNotebookValid, setIsNotebookValid] = useState<
    string | null | undefined
  >(null);
  // to abort ongoing API requests
  const fetchDataController = useRef<AbortController | undefined>();

  useEffect(() => {
    const fetchData = async () => {
      if (fetchDataController.current) {
        fetchDataController.current.abort();
      }

      setIsChecking(true);
      let validNotebook = null;
      if (props.panel && props.panel.model) {
        // only fetch when the panel has finished building
        if (props.panel.context.isReady) {
          try {
            fetchDataController.current = new AbortController();
            const signal = fetchDataController.current.signal;

            const notebookId = props.panel.model.getMetadata('notebook_id');
            const response = await fetch(
              `${BACKEND_API_URL}/dashboard/check/${notebookId}?hashedList=${hashCellList(
                props.cellIds
              )}`,
              { signal: signal }
            );

            if (!signal.aborted) {
              if (response.ok) {
                const data = await response.json();
                if (data.status === 'not_found') {
                  // no entry found in the Notebook table for the notebook_id
                  console.log('Notebook not registered');
                } else if (data.status === 'hash_mismatch') {
                  // hash mismatch between the URL parameter and the notebook table entry
                  console.log(
                    'Cell list mismatch with the registered notebook'
                  );
                } else if (data.status === 'success') {
                  validNotebook = notebookId;
                }
              }
              setIsChecking(false);
            }
          } catch (error) {
            console.log('Error:', error);
          } finally {
            // reset the controller to allow new API calls
            fetchDataController.current = undefined;
          }
        }
      }
      setIsNotebookValid(validNotebook);
    };

    // call the async fetch method
    fetchData();

    return () => {
      console.log('Clean up called');
      // clean up callback function
      if (fetchDataController.current) {
        fetchDataController.current.abort();
      }
    };
  }, [props]);

  return (
    <>
      {props.panel ? (
        <>
          {isChecking ? (
            <Loader />
          ) : (
            <>
              {isNotebookValid ? (
                <Provider store={store}>
                  <PageRouter
                    notebookId={isNotebookValid}
                    notebookName={props.panel.sessionContext.name}
                  />
                </Provider>
              ) : (
                <InvalidNotebookPlaceholder title={'Side Panel Dashboard'} />
              )}
            </>
          )}
        </>
      ) : (
        <NoNotebookPlaceholder title={'Side Panel Dashboard'} />
      )}
    </>
  );
};

export default DashboardComponent;
