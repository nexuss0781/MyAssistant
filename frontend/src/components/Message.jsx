export default function Message({ type, text, metadata }) {
  const isUser = type === 'user';

  let alignment = 'justify-content-start';
  if (isUser) alignment = 'justify-content-end';

  let bgColor = 'bg-secondary'; // Default for agent messages
  if (isUser) bgColor = 'bg-primary';
  if (type === 'agent_status') bgColor = 'bg-transparent text-secondary text-center';
  if (type === 'agent_error') bgColor = 'bg-danger';
  if (type === 'file_operation') bgColor = 'bg-info';
  if (type === 'terminal_operation') bgColor = 'bg-success';
  if (type === 'browser_operation') bgColor = 'bg-warning';

  // Special handling for status messages
  if (type === 'agent_status') {
    return (
      <div className="d-flex justify-content-center">
        <div className="p-2 mb-3 text-muted fst-italic">
          <p className="mb-0">{text}</p>
        </div>
      </div>
    );
  }

  // Special handling for tool operation messages with visual indicators
  if (['file_operation', 'terminal_operation', 'browser_operation'].includes(type)) {
    return (
      <div className="d-flex justify-content-start">
        <div className={`p-3 rounded-3 mb-3 w-75 ${bgColor} text-dark`}>
          <div className="d-flex align-items-center mb-2">
            <span className="me-2" style={{ fontSize: '16px' }}>
              {getOperationIcon(type, metadata?.status)}
            </span>
            <strong>{getOperationTitle(type)}</strong>
            {metadata?.status && (
              <span className={`ms-auto badge ${getStatusBadgeClass(metadata.status)}`}>
                {metadata.status}
              </span>
            )}
          </div>
          <div style={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace', fontSize: '13px' }}>
            {text}
          </div>
          {metadata?.duration && (
            <div className="mt-2 text-muted" style={{ fontSize: '11px' }}>
              Duration: {metadata.duration}ms
            </div>
          )}
        </div>
      </div>
    );
  }

  // Loading state for operations in progress
  if (type === 'operation_loading') {
    return (
      <div className="d-flex justify-content-start">
        <div className="p-3 rounded-3 mb-3 w-75 bg-light border">
          <div className="d-flex align-items-center">
            <div className="spinner-border spinner-border-sm me-2" role="status"></div>
            <span>{text}</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`d-flex ${alignment}`}>
      <div className={`p-3 rounded-3 mb-3 w-75 ${bgColor}`}>
        <p className="mb-0" style={{ whiteSpace: 'pre-wrap' }}>{text}</p>
      </div>
    </div>
  );
}

function getOperationIcon(type, status) {
  const icons = {
    file_operation: status === 'success' ? '📁✅' : status === 'error' ? '📁❌' : '📁⏳',
    terminal_operation: status === 'success' ? '💻✅' : status === 'error' ? '💻❌' : '💻⏳',
    browser_operation: status === 'success' ? '🌐✅' : status === 'error' ? '🌐❌' : '🌐⏳'
  };
  return icons[type] || '⚙️';
}

function getOperationTitle(type) {
  const titles = {
    file_operation: 'File Operation',
    terminal_operation: 'Terminal Command',
    browser_operation: 'Browser Action'
  };
  return titles[type] || 'Operation';
}

function getStatusBadgeClass(status) {
  const classes = {
    success: 'bg-success',
    error: 'bg-danger',
    running: 'bg-warning text-dark',
    pending: 'bg-secondary'
  };
  return classes[status] || 'bg-secondary';
}
