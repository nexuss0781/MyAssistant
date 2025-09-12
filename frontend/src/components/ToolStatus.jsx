import React from 'react';

const ToolStatus = ({ activeOperations }) => {
  if (!activeOperations || activeOperations.length === 0) {
    return null;
  }

  return (
    <div className="position-fixed" style={{ 
      bottom: '20px', 
      right: '20px', 
      zIndex: 1000,
      maxWidth: '300px'
    }}>
      {activeOperations.map((operation, index) => (
        <div key={index} className="alert alert-info alert-dismissible fade show mb-2" role="alert">
          <div className="d-flex align-items-center">
            <div className="spinner-border spinner-border-sm me-2" role="status"></div>
            <div>
              <strong>{getOperationTitle(operation.type)}</strong>
              <div className="small text-muted">{operation.description}</div>
              {operation.progress && (
                <div className="progress mt-1" style={{ height: '4px' }}>
                  <div 
                    className="progress-bar" 
                    role="progressbar" 
                    style={{ width: `${operation.progress}%` }}
                    aria-valuenow={operation.progress} 
                    aria-valuemin="0" 
                    aria-valuemax="100"
                  ></div>
                </div>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

function getOperationTitle(type) {
  const titles = {
    file_operation: '📁 File Operation',
    terminal_operation: '💻 Terminal',
    browser_operation: '🌐 Browser',
    ai_thinking: '🤖 AI Processing'
  };
  return titles[type] || '⚙️ Operation';
}

export default ToolStatus;