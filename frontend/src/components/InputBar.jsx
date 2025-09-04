// frontend/src/components/InputBar.jsx
import { useState } from 'react';

export default function InputBar({ onSubmit, isRunning }) {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (prompt.trim()) {
      onSubmit(prompt);
      setPrompt(''); // Clear the input after submitting
    }
  };

  return (
    <div className="p-3 bg-body-tertiary">
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <textarea
            className="form-control bg-dark text-white"
            placeholder={isRunning ? "Agent is working..." : "Enter your prompt here..."}
            rows="1"
            style={{ resize: 'none' }}
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            disabled={isRunning} // Disable input while agent is running
          ></textarea>
          <button className="btn btn-primary" type="submit" disabled={isRunning}>
            {isRunning ? 'Running...' : 'Send'}
          </button>
        </div>
      </form>
    </div>
  );
}
