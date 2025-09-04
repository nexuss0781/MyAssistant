export default function Message({ type, text }) {
  const isUser = type === 'user';

  let alignment = 'justify-content-start';
  if (isUser) alignment = 'justify-content-end';

  let bgColor = 'bg-secondary'; // Default for agent messages
  if (isUser) bgColor = 'bg-primary';
  if (type === 'agent_status') bgColor = 'bg-transparent text-secondary text-center';
  if (type === 'agent_error') bgColor = 'bg-danger';

  if (type === 'agent_status') {
    return (
      <div className="d-flex justify-content-center">
        <div className="p-2 mb-3 text-muted fst-italic">
          <p className="mb-0">{text}</p>
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
