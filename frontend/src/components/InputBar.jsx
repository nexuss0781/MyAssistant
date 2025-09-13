import { useState, useRef, useEffect } from 'react';

export default function InputBar({ onSubmit, isRunning }) {
  const [prompt, setPrompt] = useState('');
  const editableDivRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (prompt.trim()) {
      onSubmit(prompt);
      setPrompt('');
      if (editableDivRef.current) {
        editableDivRef.current.textContent = '';
      }
    }
  };

  const handleInput = (e) => {
    setPrompt(e.target.textContent);
  };

  return (
    <div className="p-3 bg-light border-top">
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <div
            ref={editableDivRef}
            className="form-control"
            contentEditable={!isRunning}
            onInput={handleInput}
            placeholder={isRunning ? "Agent is working..." : "Enter your prompt here..."}
            style={{ minHeight: '40px', maxHeight: '200px', overflowY: 'auto' }}
          ></div>
          <button className="btn btn-primary" type="submit" disabled={isRunning}>
            {isRunning ? <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> : <i className="bi bi-send"></i>}
          </button>
        </div>
      </form>
    </div>
  );
}
