import React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { ITranslator, nullTranslator } from '@jupyterlab/translation';
import { ActivityMonitor, PathExt } from '@jupyterlab/coreutils';
import { Message } from '@lumino/messaging';
import { NotebookPanel } from '@jupyterlab/notebook';
import { TOC_DASHBOARD_RENDER_TIMEOUT } from '../utils/constants';
import DashboardComponent from './dashboardComponent';

class DashboardSidePanel extends ReactWidget {
  constructor(translator: ITranslator | undefined) {
    super();

    this.addClass('dashboard-react-widget');

    this._panel = null;
    this._monitor = null;
    this._cellIds = null;
  }

  get panel(): NotebookPanel | null {
    return this._panel;
  }

  set panel(value: NotebookPanel | null) {
    if (value && this._panel && this._panel === value) {
      return;
    }

    if (this._panel) {
      this._panel.disposed.disconnect(this._onPanelDisposed, this);
    }

    this._panel = value;

    if (this._panel) {
      this._panel.disposed.connect(this._onPanelDisposed, this);
    }

    // dispose an old activity monitor if one existed...
    if (this._monitor) {
      this._monitor.dispose();
      this._monitor = null;
    }
    // if we are wiping the ToC dashboard, update and return...
    if (!this._panel) {
      this.update();
      return;
    }

    const context = this._panel.context;

    // throttle the rendering rate of the table of contents:
    this._monitor = new ActivityMonitor({
      signal: context.model.contentChanged,
      timeout: TOC_DASHBOARD_RENDER_TIMEOUT
    });
    this._monitor.activityStopped.connect(this.update, this);
    this.update();
  }

  private _onPanelDisposed(_panel: NotebookPanel) {
    // when the panel is disposed, dispose from the toc panel (calling the _panel setter)
    this.panel = null;
  }

  protected onAfterShow(msg: Message): void {
    this.update();
  }

  protected onUpdateRequest(msg: Message): void {
    this.updateCellList();

    // this calls render() through the parent class
    super.onUpdateRequest(msg);
  }

  private updateCellList() {
    if (this._panel) {
      const cells = this._panel.model?.cells;
      this._cellIds = cells ? Array.from(cells).map(c => c.id) : null;
    } else {
      this._cellIds = null;
    }
  }

  render(): JSX.Element {
    return <DashboardComponent panel={this._panel} cellIds={this._cellIds} />;
  }

  private _panel: NotebookPanel | null;
  private _monitor: ActivityMonitor<any, any> | null;
  private _cellIds: string[] | null;
}

export default DashboardSidePanel;
