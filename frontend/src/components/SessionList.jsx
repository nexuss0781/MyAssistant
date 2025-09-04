// This component is now 'dumb' - it just renders the props it's given.
// All logic is handled by its parent, App.jsx.
export default function SessionList({ sessions, activeSessionId, onNewSession, onSelectSession }) {
  return (
    <div className="d-flex flex-column h-100 p-3 bg-body-tertiary">
      <h2 className="fs-5 mb-3">Sessions</h2>
      
      <button className="btn btn-outline-primary w-100 mb-3" onClick={onNewSession}>
        + New Chat
      </button>

      {/* List of Sessions, rendered from props */}
      <ul className="nav nav-pills flex-column mb-auto">
        {sessions.map((session) => (
          <li className="nav-item" key={session.id}>
            <a 
              href="#" 
              // Use the 'active' class if this is the currently active session
              className={`nav-link text-white ${activeSessionId === session.id ? 'active' : ''}`}
              onClick={(e) => {
                e.preventDefault();
                onSelectSession(session.id);
              }}
            >
              {session.name}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
