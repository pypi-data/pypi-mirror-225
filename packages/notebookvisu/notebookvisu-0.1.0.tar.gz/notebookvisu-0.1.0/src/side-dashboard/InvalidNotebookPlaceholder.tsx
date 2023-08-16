import React from 'react';

const InvalidNotebookPlaceholder = ({
  title
}: {
  title: string;
}): JSX.Element => {
  return (
    <div className="dashboard-TableOfContents">
      <div className="dashboard-stack-panel-header">{title}</div>
      <div className="dashboard-TableOfContents-placeholder">
        <div className="dashboard-TableOfContents-placeholderContent">
          <h3>Invalid Notebook</h3>
          <p>No data found on the server for the opened notebook.</p>
        </div>
      </div>
    </div>
  );
};

export default InvalidNotebookPlaceholder;
