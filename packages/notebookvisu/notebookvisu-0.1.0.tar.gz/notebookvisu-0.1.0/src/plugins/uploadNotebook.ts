import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import {
  PluginIDs,
  CommandIDs,
  notebookSelector,
  BACKEND_API_URL
} from '../utils/constants';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { fileUploadIcon } from '@jupyterlab/ui-components';
import { showDialog, Dialog } from '@jupyterlab/apputils';
import { IMainMenu } from '@jupyterlab/mainmenu';
import { Menu } from '@lumino/widgets';
import { v4 as uuidv4 } from 'uuid';
import JSZip from 'jszip';

function generateNotebookId(): string {
  return uuidv4();
}

function compressAndUploadNotebook(
  notebookContent: any,
  notebookName: string,
  notebookId: string,
  cells: string[]
): Promise<any> {
  return new Promise((resolve, reject) => {
    const zip = new JSZip();
    zip.file(notebookName, JSON.stringify(notebookContent));

    zip
      .generateAsync({ type: 'blob' })
      .then((compressedZip: Blob) => {
        const formData = new FormData();
        formData.append('zipped_content', compressedZip);
        formData.append('notebook_id', notebookId);
        formData.append('name', notebookName);
        formData.append('cells', JSON.stringify(cells));

        const url = BACKEND_API_URL + '/notebook/upload';
        fetch(url, {
          method: 'POST',
          body: formData
        })
          .then(response => {
            if (response.ok) {
              resolve(response.json()); // resolve the promise with the response data
            } else {
              reject(new Error('Failed to upload notebook on the backend')); // reject the promise with an error
            }
          })
          .catch(error => {
            console.error('Error occurred while uploading notebook:', error);
            reject(error);
          });
      })
      .catch(error => {
        console.error('Error occurred while compressing notebook:', error);
        reject(error);
      });
  });
}

function activateUpload(
  app: JupyterFrontEnd,
  factory: IFileBrowserFactory,
  mainMenu: IMainMenu
) {
  console.log('JupyterLab extension upload is activated!');

  app.commands.addCommand(CommandIDs.uploadNotebook, {
    label: 'Upload notebook for dashboard tracking',
    icon: args => (args['isContextMenu'] ? fileUploadIcon : undefined),
    execute: args => {
      console.log('Upload Notebook');
      const file = factory.tracker.currentWidget?.selectedItems().next().value;

      if (file) {
        app.serviceManager.contents.get(file.path).then(getResponse => {
          const cells = getResponse.content.cells.map((item: any) => item.id);
          getResponse.content.metadata['notebook_id'] ??= generateNotebookId(); // only modify if there is no notebook_id
          // getResponse.content.metadata['notebook_id'] = generateNotebookId();

          const cellMapping: [string, string][] = cells.map(
            (cellId: string) => [cellId, cellId]
          );
          getResponse.content.metadata['cell_mapping'] = cellMapping;

          // save the tagged notebook and wait for it to be saved before sending to the server
          app.serviceManager.contents
            .save(file.path, getResponse)
            .then(saveResponse => {
              compressAndUploadNotebook(
                getResponse.content,
                file.name,
                getResponse.content.metadata['notebook_id'],
                cells
              )
                .then(responseData => {
                  console.log(responseData);
                  showDialog({
                    title: file.name,
                    body: 'File uploaded to the server',
                    buttons: [Dialog.okButton()]
                  }).catch(e => console.log(e));
                })
                .catch(e => {
                  showDialog({
                    title: file.name,
                    body: 'Error uploading the file',
                    buttons: [Dialog.cancelButton()]
                  }).catch(e => console.log(e));
                });
            });
        });
      }
    }
  });

  app.contextMenu.addItem({
    selector: notebookSelector,
    type: 'separator',
    rank: 0
  });
  app.contextMenu.addItem({
    args: { isContextMenu: true },
    command: CommandIDs.uploadNotebook,
    selector: notebookSelector,
    rank: 0
  });
  app.contextMenu.addItem({
    selector: notebookSelector,
    type: 'separator',
    rank: 0
  });

  const menu = new Menu({ commands: app.commands });
  menu.title.label = 'Dashboard';

  menu.addItem({
    command: CommandIDs.uploadNotebook,
    args: { isContextMenu: false }
  });
  mainMenu.addMenu(menu, true, { rank: 40 });
}

const uploadNotebookPlugin: JupyterFrontEndPlugin<void> = {
  id: PluginIDs.uploadNotebookPlugin,
  autoStart: true,
  requires: [IFileBrowserFactory, IMainMenu],
  activate: activateUpload
};

export default uploadNotebookPlugin;
