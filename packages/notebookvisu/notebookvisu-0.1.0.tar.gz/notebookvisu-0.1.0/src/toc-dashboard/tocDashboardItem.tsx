import React from 'react';
import { INotebookHeading } from '../utils/headings';
import { Signal } from '@lumino/signaling';
import { TocDashboardPanel } from './tocDashboardPanel';
import { ItemRenderer } from '../utils/interfaces';
import TocReactComponent from './TocReactComponent';
import { connect } from 'react-redux';
import { RootState } from '../redux/store';

interface ITocDashboardItemProps {
  heading: INotebookHeading;

  headings: INotebookHeading[];

  entryClicked?: Signal<TocDashboardPanel, TocDashboardItem>;

  itemRenderer: ItemRenderer;

  tocDashboardData: number[] | null;

  shouldDisplayRedux: boolean;
}

interface IState {}

const mapStateToProps = (state: RootState) => {
  return {
    shouldDisplayRedux: state.tocdashboard.displayDashboard
  };
};

export class TocDashboardItem extends React.Component<
  ITocDashboardItemProps,
  IState
> {
  render() {
    const { heading, headings, tocDashboardData, shouldDisplayRedux } =
      this.props;

    // create an onClick handler for the TOC item
    // that scrolls the anchor into view.
    const onClick = (event: React.SyntheticEvent<HTMLSpanElement>) => {
      event.preventDefault();
      event.stopPropagation();
      this.props.entryClicked?.emit(this);
      heading.onClick();
    };

    let content = this.props.itemRenderer(heading, headings);
    if (!content) {
      return null;
    }
    return (
      <li
        className="dashboard-tocItem"
        onClick={onClick}
        onContextMenu={(event: React.SyntheticEvent<HTMLSpanElement>) => {
          this.props.entryClicked?.emit(this);
          heading.onClick();
        }}
      >
        {content}
        {shouldDisplayRedux && tocDashboardData && (
          <TocReactComponent
            cellId={heading.cellRef.model.id}
            users={tocDashboardData[0]}
            total_users={tocDashboardData[1]}
          />
        )}
      </li>
    );
  }
}

export const ConnectedTocDashboardItem =
  connect(mapStateToProps)(TocDashboardItem);
