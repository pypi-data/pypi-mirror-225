import { Message } from '@lumino/messaging';
import { ActivityMonitor, PathExt } from '@jupyterlab/coreutils';
import { Widget } from '@lumino/widgets';
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { Signal } from '@lumino/signaling';
import {
  ITranslator,
  TranslationBundle,
  nullTranslator
} from '@jupyterlab/translation';
import { NotebookPanel } from '@jupyterlab/notebook';
import { TOC_DASHBOARD_RENDER_TIMEOUT } from '../utils/constants';
import { INotebookHeading } from '../utils/headings';
import TocDashboardTree from './tocDashboardTree';
import { TocDashboardItem } from './tocDashboardItem';
import { ICurrentPanel } from '../utils/interfaces';
import { Provider } from 'react-redux';
import { store } from '../redux/store';
import NoNotebookPlaceholder from './NoNotebookPlaceholder';
import { ToolbarComponent } from './generator/toolbar_generator';

export class TocDashboardPanel extends Widget {
  constructor(translator: ITranslator | null) {
    super();
    this._trans = (translator || nullTranslator).load('jupyterlab');
    this._headings = [];
    this._entryClicked = new Signal<TocDashboardPanel, TocDashboardItem>(this);
    this._entryClicked.connect((dashboard, item) => {
      this.activeEntry = item.props.heading;
    });
    this._current = null;
    this._activeEntry = null;
    this._monitor = null;
    this._toolbar = null;
  }

  get current(): ICurrentPanel | null {
    return this._current;
  }

  set current(value: ICurrentPanel | null) {
    // if they are the same as previously, do nothing
    if (
      value &&
      this._current &&
      this._current.panel === value.panel &&
      this._current.notebookGenerator === value.notebookGenerator
    ) {
      return;
    }

    if (this._current) {
      this._current.panel.disposed.disconnect(this._onPanelDisposed, this);
    }

    this._current = value;

    if (this._current) {
      this._current.panel.disposed.connect(this._onPanelDisposed, this);
    }

    if (this.notebookGenerator) {
      if (this.notebookGenerator.toolbarGenerator) {
        this._toolbar = this.notebookGenerator.toolbarGenerator();
      } else {
        this._toolbar = null;
      }
    }
    // dispose an old activity monitor if one existed...
    if (this._monitor) {
      this._monitor.dispose();
      this._monitor = null;
    }
    // if we are wiping the ToC dashboard, update and return...
    if (!this._current) {
      this.update();
      return;
    }

    const context = this._current.panel.context;

    // Throttle the rendering rate of the table of contents:
    this._monitor = new ActivityMonitor({
      signal: context.model.contentChanged,
      timeout: TOC_DASHBOARD_RENDER_TIMEOUT
    });
    this._monitor.activityStopped.connect(this.update, this);
    this.update();
  }

  private _onPanelDisposed(_panel: NotebookPanel) {
    // when the panel is disposed, dispose from the toc panel (calling the _current setter)
    this.current = null;
  }

  get notebookGenerator() {
    if (this._current) {
      return this._current.notebookGenerator;
    }
    return null;
  }

  protected onUpdateRequest(msg: Message): void {
    let title = this._trans.__('Dashboard ToC');

    if (this._current) {
      this._headings = this._current.notebookGenerator.generate(
        this._current.panel
      );
      const context = this._current.panel.context;
      if (context) {
        title = PathExt.basename(context.localPath);
      }
    }
    let itemRenderer: (
      item: INotebookHeading,
      headings: INotebookHeading[]
    ) => JSX.Element | null = (item: INotebookHeading) => {
      return <span>{item.text}</span>;
    };
    if (this._current && this._current.notebookGenerator.itemRenderer) {
      itemRenderer = this._current.notebookGenerator.itemRenderer;
    }
    let jsx = <NoNotebookPlaceholder title={title} />;
    if (
      this._current &&
      this._current.notebookGenerator &&
      this._current.panel
    ) {
      jsx = (
        <Provider store={store}>
          <TocDashboardTree
            title={title}
            headings={this._headings}
            entryClicked={this._entryClicked}
            itemRenderer={itemRenderer}
            Toolbar={this._toolbar}
            notebookModel={this._current.panel.model}
          />
        </Provider>
      );
    }
    ReactDOM.render(jsx, this.node);
  }

  get activeEntry(): INotebookHeading | null {
    return this._activeEntry;
  }

  set activeEntry(value: INotebookHeading | null) {
    this._activeEntry = value;
  }

  get headings(): INotebookHeading[] {
    return this._headings;
  }

  protected onAfterShow(msg: Message): void {
    this.update();
  }

  private _trans: TranslationBundle;
  private _current: ICurrentPanel | null;
  private _headings: INotebookHeading[];
  private _toolbar: ToolbarComponent | null;

  private _activeEntry: INotebookHeading | null;
  private _entryClicked?: Signal<TocDashboardPanel, TocDashboardItem>;
  private _monitor: ActivityMonitor<any, any> | null;
}
