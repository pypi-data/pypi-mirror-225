import { DocumentRegistry } from '@jupyterlab/docregistry';
import { IDisposable, DisposableDelegate } from '@lumino/disposable';
import { NotebookPanel, INotebookModel } from '@jupyterlab/notebook';
import { CommandIDs } from '../utils/constants';
import { ToolbarButton } from '@jupyterlab/apputils';
import { analyticsIcon } from '../icons';
import { CommandRegistry } from '@lumino/commands';

export class NotebookButton
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel>
{
  private _commands: CommandRegistry;

  constructor(commands: CommandRegistry) {
    this._commands = commands;
  }

  /**
   * Create a new extension for the notebook panel widget.
   *
   * @param panel Notebook panel
   * @param context Notebook context
   * @returns Disposable on the added button
   */
  createNew(
    panel: NotebookPanel,
    context: DocumentRegistry.IContext<INotebookModel>
  ): IDisposable {
    const button = new ToolbarButton({
      className: 'open-visu-button',
      icon: analyticsIcon,
      onClick: () => {
        let notebook_id = context.model.metadata['notebook_id'];
        const notebook_name = context.sessionContext.name;
        this._commands.execute(CommandIDs.dashboardOpenVisu, {
          from: 'Notebook',
          notebook_id: notebook_id as string,
          notebook_name: notebook_name
        });
      },
      tooltip: 'Open Notebook Visualization'
    });

    panel.toolbar.insertItem(10, 'openVisu', button);

    return new DisposableDelegate(() => {
      button.dispose();
    });
  }
}
