import React, { useState, useEffect } from 'react';
import { Row, Col } from 'react-bootstrap';
import { BACKEND_API_URL } from '../../utils/constants';
import { ChartData } from 'chart.js';
import { useSelector } from 'react-redux';
import { RootState } from '../../redux/store';
import { Bar, Scatter } from 'react-chartjs-2';
import {
  locationOptions,
  codeExecOptions,
  timeSpentOptions
} from '../../utils/chartOptions';
import ChartContainer from '../components/notebook/ChartContainer';
import TimeDropDown from '../components/buttons/TimeDropDown';

const Notebook = (props: {
  notebookId: string;
  notebookName: string;
}): JSX.Element => {
  const navigationState = useSelector(
    (state: RootState) => state.sidedashboard.navigationState
  );
  const timeWindow = useSelector(
    (state: RootState) => state.sidedashboard.timeWindow
  );

  // const notebookId = props.panel.model?.getMetadata('notebook_id');
  // const notebookName = props.panel.context.sessionContext.name;

  const [locationData, setLocationData] = useState<ChartData<'bar'>>({
    labels: [],
    datasets: []
  });
  const [codeExecData, setCodeExecData] = useState<ChartData<'bar'>>({
    labels: [],
    datasets: []
  });
  const [timeSpentData, setTimeSpentData] = useState<ChartData<'scatter'>>({
    labels: [],
    datasets: []
  });

  const [isLocationFetching, setIsLocationFetching] = useState(false);
  const [isCodeExecFetching, setIsCodeExecFetching] = useState(false);
  const [isTimeSpentFetching, setIsTimeSpentFetching] = useState(false);

  // fetching location data
  useEffect(() => {
    setIsLocationFetching(true);
    fetch(
      `${BACKEND_API_URL}/dashboard/${props.notebookId}/user_location?timeWindow=${timeWindow}`
    )
      .then(response => response.json())
      .then(data => {
        const chartData: ChartData<'bar'> = {
          labels: data.map((item: any, index: number) => index + 1),
          datasets: [
            {
              label: 'Number of users',
              data: data.map((item: any) => item.instance_ids.length),
              backgroundColor: 'rgba(54, 162, 235, 0.2)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1
            }
          ]
        };
        setLocationData(chartData);
        setIsLocationFetching(false);
      });
  }, [navigationState, timeWindow]);

  // fetching execution data
  useEffect(() => {
    setIsCodeExecFetching(true);
    fetch(
      `${BACKEND_API_URL}/dashboard/${props.notebookId}/user_code_execution?timeWindow=${timeWindow}`
    )
      .then(response => response.json())
      .then(data => {
        const chartData: ChartData<'bar'> = {
          labels: data.map((item: any, index: number) => index + 1),
          datasets: [
            {
              label: '% accessed',
              data: data.map((item: any) => parseFloat(item.cell_click_pct)),
              backgroundColor: 'rgba(54, 162, 235, 0.2)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1
            },
            {
              label: '% executed',
              data: data.map((item: any) => parseFloat(item.code_exec_pct)),
              backgroundColor: 'rgba(255, 99, 132, 0.2)',
              borderColor: 'rgba(255,99,132,1)',
              borderWidth: 1
            },
            {
              label: '% executed without errors',
              data: data.map((item: any) => parseFloat(item.code_exec_ok_pct)),
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1
            }
          ]
        };
        setCodeExecData(chartData);
        setIsCodeExecFetching(false);
      });
  }, [navigationState, timeWindow]);

  // fetching access time data
  useEffect(() => {
    setIsTimeSpentFetching(true);
    fetch(
      `${BACKEND_API_URL}/dashboard/${props.notebookId}/user_cell_time?timeWindow=${timeWindow}`
    )
      .then(response => response.json())
      .then(data => {
        const chartData: ChartData<'scatter'> = {
          labels: data.map((item: any, index: number) => index + 1),
          datasets: [
            {
              label: 'time spent on a cell by a user',
              data: data.flatMap((item: any, index: number) =>
                item.durations.map((duration: number) => ({
                  x: index + 1,
                  y: duration
                }))
              ),
              backgroundColor: 'rgba(54, 162, 235, 0.2)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1,
              pointRadius: 1
            }
          ]
        };
        setTimeSpentData(chartData);
        setIsTimeSpentFetching(false);
      });
  }, [navigationState, timeWindow]);

  return (
    <>
      <div className="course-title-container">
        {props.notebookName}
        <TimeDropDown />
      </div>
      <Row>
        <Col>
          <Row className="mb-4">
            <ChartContainer
              isFetching={isTimeSpentFetching}
              isNotEmpty={timeSpentData.labels?.length}
              PassedComponent={
                <Scatter
                  className="scatter-test"
                  data={timeSpentData}
                  options={timeSpentOptions}
                />
              }
              title="Amount of time spent on each cell"
              noDataText="No cell access time data in selected time window"
            />
          </Row>
          <Row className="mb-4">
            <ChartContainer
              isFetching={isLocationFetching}
              isNotEmpty={locationData.labels?.length}
              PassedComponent={
                <Bar data={locationData} options={locationOptions} />
              }
              title="Location of users across the notebook"
              noDataText="No location data in selected time window"
            />
          </Row>
          <Row className="mb-4">
            <ChartContainer
              isFetching={isCodeExecFetching}
              isNotEmpty={codeExecData.labels?.length}
              PassedComponent={
                <Bar data={codeExecData} options={codeExecOptions} />
              }
              title="Code cell execution across users"
              noDataText="No cell execution data in selected time window"
            />
          </Row>
        </Col>
      </Row>
    </>
  );
};

export default Notebook;
