import * as React from 'react';
import { INotebookTracker, NotebookActions } from '@jupyterlab/notebook';
import { OptionsManager } from './options_manager';
import { INotebookHeading } from '../../utils/headings';
import {
  sanitizerOptions,
  MARKDOWN_HEADING_COLLAPSED,
  UNSYNC_MARKDOWN_HEADING_COLLAPSED
} from './utils';
import CellInput from '../../side-dashboard/components/cell/CellInput';

function render(
  options: OptionsManager,
  tracker: INotebookTracker,
  item: INotebookHeading,
  headings: INotebookHeading[] = []
) {
  let jsx;
  if (item.type === 'markdown' || item.type === 'header') {
    let fontSizeClass = 'dashboard-toc-level-size-default';
    let numbering = item.numbering && options.numbering ? item.numbering : '';
    let cellCollapseMetadata = options.syncCollapseState
      ? MARKDOWN_HEADING_COLLAPSED
      : UNSYNC_MARKDOWN_HEADING_COLLAPSED;
    if (item.type === 'header') {
      fontSizeClass = 'dashboard-toc-level-size-' + item.level;
    }
    if (item.html && (item.type === 'header' || options.showMarkdown)) {
      jsx = (
        <span
          dangerouslySetInnerHTML={{
            __html:
              numbering +
              options.sanitizer.sanitize(item.html, sanitizerOptions)
          }}
          className={item.type + '-cell dashboard-toc-cell-item'}
        />
      );
      // render the headers
      if (item.type === 'header') {
        let button = (
          <div
            className="jp-Collapser p-Widget lm-Widget"
            onClick={(event: any) => {
              event.stopPropagation();
              onClick(tracker, cellCollapseMetadata, item);
            }}
          >
            <div className="dashboard-toc-Collapser-child" />
          </div>
        );

        // render the heading item
        jsx = (
          <div
            className={
              'dashboard-toc-entry-holder ' +
              fontSizeClass +
              (tracker.activeCell === item.cellRef
                ? ' dashboard-toc-active-cell'
                : previousHeader(tracker, item, headings)
                ? ' dashboard-toc-active-cell'
                : '')
            }
          >
            {button}
            {jsx}
          </div>
        );
      }
      return jsx;
    }
    if (item.type === 'header' || options.showMarkdown) {
      // render headers/markdown for plain text
      jsx = (
        <span className={item.type + '-cell dashboard-toc-cell-item'}>
          {numbering + item.text}
        </span>
      );
      if (item.type === 'header') {
        let button = (
          <div
            className="jp-Collapser p-Widget lm-Widget"
            onClick={(event: any) => {
              event.stopPropagation();
              onClick(tracker, cellCollapseMetadata, item);
            }}
          >
            <div className="dashboard-toc-Collapser-child" />
          </div>
        );

        jsx = (
          <div
            className={
              'dashboard-toc-entry-holder ' +
              fontSizeClass +
              (tracker.activeCell === item.cellRef
                ? ' dashboard-toc-active-cell'
                : previousHeader(tracker, item, headings)
                ? ' dashboard-toc-active-cell'
                : '')
            }
          >
            {button}
            {jsx}
          </div>
        );
      }
      return jsx;
    }
    return null;
  }
  if (tracker.currentWidget && item.type === 'code' && options.showCode) {
    // render code cells

    // if undefined, display as text
    const language_mimetype =
      tracker.currentWidget.model?.metadata.language_info?.mimetype || 'text';
    return (
      <div className="dashboard-toc-code-cell-div">
        <div className="dashboard-toc-code-cell-prompt">{item.prompt}</div>
        <span className={'dashboard-toc-code-span'}>
          <CellInput
            cell_input={item.text}
            language_mimetype={language_mimetype}
            className="dashboard-toc-cell-input"
          />
        </span>
      </div>
    );
  }
  return null;

  function onClick(
    tracker: INotebookTracker,
    cellCollapseMetadata: string,
    heading?: INotebookHeading
  ) {
    let collapsed = false;
    let syncCollapseState = options.syncCollapseState;
    if (heading?.cellRef.model.getMetadata(cellCollapseMetadata)) {
      collapsed = heading.cellRef.model.getMetadata(
        cellCollapseMetadata
      ) as boolean;
    }
    if (heading) {
      if (syncCollapseState) {
        // if collapse state is synced, update state here
        if (tracker.currentWidget) {
          NotebookActions.setHeadingCollapse(
            heading!.cellRef!,
            !collapsed,
            tracker.currentWidget.content
          );
        }
      } else {
        if (collapsed) {
          heading.cellRef.model.deleteMetadata(cellCollapseMetadata);
        } else {
          heading.cellRef.model.setMetadata(cellCollapseMetadata, true);
        }
      }
      options.updateAndCollapse({
        heading: heading,
        collapsedState: collapsed
      });
    } else {
      options.updateWidget();
    }
  }
}

function previousHeader(
  tracker: INotebookTracker,
  item: INotebookHeading,
  headings: INotebookHeading[]
) {
  if (item.index > -1 || headings?.length) {
    let activeCellIndex = tracker.currentWidget!.content.activeCellIndex;
    let headerIndex = item.index;
    // header index has to be less than the active cell index
    if (headerIndex < activeCellIndex) {
      let tocIndexOfNextHeader = headings.indexOf(item) + 1;
      // return true if header is the last header
      if (tocIndexOfNextHeader >= headings.length) {
        return true;
      }
      // return true if the next header cells index is greater than the active cells index
      let nextHeaderIndex = headings?.[tocIndexOfNextHeader].index;
      if (nextHeaderIndex > activeCellIndex) {
        return true;
      }
    }
  }
  return false;
}

export { render };
