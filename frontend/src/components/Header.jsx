// A simple SVG for the hamburger icon
const MenuIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" className="bi bi-list" viewBox="0 0 16 16">
    <path fillRule="evenodd" d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5"/>
  </svg>
);

export default function Header() {
  return (
    // This header is only visible on screens smaller than md (d-md-none)
    <header className="d-md-none p-3 bg-body-tertiary d-flex justify-content-between align-items-center">
      <h1 className="fs-5 mb-0">AI Agent</h1>
      <button 
        className="btn" 
        type="button" 
        data-bs-toggle="offcanvas" 
        data-bs-target="#session-sidebar" 
        aria-controls="session-sidebar"
        aria-label="Toggle navigation"
      >
        <MenuIcon />
      </button>
    </header>
  );
}
