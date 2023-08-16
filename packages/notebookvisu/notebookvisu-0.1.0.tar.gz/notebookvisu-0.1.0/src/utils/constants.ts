// export const BACKEND_API_URL = 'https://unianalytics.ch';
export const BACKEND_API_URL = 'http://localhost:5000';

// adapt the app ids in the schema/*.json if this value is changed
export const APP_ID = 'notebookvisu';

export const STORAGE_KEY = `@jupyterlab/${APP_ID}:sidedashboard`;

export const TOC_DASHBOARD_RENDER_TIMEOUT = 1000;

// A plugin id has to be of the form APP_ID:<schema name without .json>
export namespace PluginIDs {
  export const sideDashboardPlugin = `${APP_ID}:sideDashboardPlugin`;

  export const tocDashboardPlugin = `${APP_ID}:tocDashboardPlugin`;

  export const themePlugin = `${APP_ID}:themePlugin`;

  export const uploadNotebookPlugin = `${APP_ID}:uploadNotebookPlugin`;
}

export namespace CommandIDs {
  export const dashboardOpenVisu = `${APP_ID}:dashboard-open-visu`;

  export const uploadNotebook = `${APP_ID}:dashboard-upload-notebook`;

  export const showDashboardToCPanel = `${APP_ID}:dashboard-toc-open-panel`;

  export const runCells = `${APP_ID}:dashboard-toc-run-cells`;
}

export const visuIconClass = 'jp-icon3';

export const notebookSelector: string =
  '.jp-DirListing-item[data-file-type="notebook"]';
