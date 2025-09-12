import { useState, useEffect, useRef } from 'react';
import { useWebSocket } from './hooks/useWebSocket';
import SessionList from './components/SessionList';
import ChatLog from './components/ChatLog';
import InputBar from './components/InputBar';
import Header from './components/Header';
import { PanelGroup, Panel, PanelResizeHandle } from 'react-resizable-panels';
import Editor from '@monaco-editor/react';

function App() {
  // --- STATE MANAGEMENT ---
  const [clientId] = useState(() => `client_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
  const [messages, setMessages] = useState([]);
  const [isAgentRunning, setIsAgentRunning] = useState(false);
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [layoutMode, setLayoutMode] = useState('simple'); // 'simple' or 'vscode'
  const [activeFileContent, setActiveFileContent] = useState('');
  const [activeFilePath, setActiveFilePath] = useState('');

  // --- WEB SOCKET HANDLING ---
  const lastMessage = useWebSocket(clientId);

  useEffect(() => {
    // Logic for handling incoming WebSocket messages (remains unchanged)
    if (!lastMessage) return;

    const parsePlanToTasks = (planText) => (
      planText.split('\n')
        .filter(line => line.trim().startsWith('- [ ]'))
        .map(line => ({ description: line.trim().substring(6), isCompleted: false }))
    );

    switch (lastMessage.type) {
      case 'status':
        setMessages(prev => [...prev, { type: 'agent_status', text: lastMessage.data }]);
        break;
      case 'plan': {
        const initialTasks = parsePlanToTasks(lastMessage.data);
        setMessages(prev => [...prev, { type: 'agent_plan', tasks: initialTasks }]);
        break;
      }
      case 'task_complete': {
        const completedTaskDesc = lastMessage.data.trim().substring(6);
        setMessages(msgs => msgs.map(msg => {
          if (msg.type === 'agent_plan') {
            const newTasks = msg.tasks.map(task =>
              task.description === completedTaskDesc ? { ...task, isCompleted: true } : task
            );
            return { ...msg, tasks: newTasks };
          }
          return msg;
        }));
        break;
      }
      case 'finish':
        setMessages(prev => [...prev, { type: 'agent', text: lastMessage.data }]);
        setIsAgentRunning(false);
        break;
      case 'error':
        setMessages(prev => [...prev, { type: 'agent_error', text: lastMessage.data }]);
        setIsAgentRunning(false);
        break;
    }
  }, [lastMessage]);

  // --- SESSION DATA FETCHING ---
  
  // Effect to fetch all sessions on initial app load
  useEffect(() => {
    const fetchSessions = async () => {
      try {
        const response = await fetch('http://localhost:8000/sessions');
        if (!response.ok) throw new Error('Failed to fetch sessions');
        const data = await response.json();
        setSessions(data);
        if (data.length > 0 && !activeSessionId) {
          setActiveSessionId(data[0].id);
        } else if (data.length === 0) {
            handleNewSession(); // Create a new session if none exist
        }
      } catch (error) {
        console.error("Error fetching sessions:", error);
      }
    };
    fetchSessions();
  }, [activeSessionId]);

  // Effect to fetch the history when the active session changes
  useEffect(() => {
    if (!activeSessionId) return;

    const fetchHistory = async () => {
        setIsAgentRunning(false); // Reset running state when switching
        try {
            const response = await fetch(`http://localhost:8000/sessions/${activeSessionId}`);
            if (!response.ok) throw new Error('Failed to fetch history');
            const history = await response.json();

            // Convert raw history into messages for the UI
            const newMessages = history.map(item => {
                if (item.type === 'agent_plan_text') {
                    const tasks = item.text.split('\n').filter(line => line.startsWith('- [ ]')).map(line => ({ description: line.substring(6).trim(), isCompleted: true }));
                    return { type: 'agent_plan', tasks };
                }
                return { type: item.type, text: item.text };
            }).filter(Boolean); // Filter out any null/undefined entries

            setMessages(newMessages);

        } catch (error) {
            console.error(`Error fetching history for ${activeSessionId}:`, error);
            setMessages([{ type: 'agent_error', text: `Failed to load session history.`}]);
        }
    };

    fetchHistory();
  }, [activeSessionId]);

  // --- EVENT HANDLERS ---
  const handleSelectSession = (sessionId) => {
    setActiveSessionId(sessionId);
  };
  
  const handleNewSession = async () => {
    try {
        const response = await fetch('http://localhost:8000/sessions', { method: 'POST' });
        if (!response.ok) throw new Error('Failed to create session');
        const newSession = await response.json();
        setSessions(prev => [newSession, ...prev]);
        setActiveSessionId(newSession.id);
    } catch (error) {
        console.error("Error creating new session:", error);
    }
  };

  const handleAgentSubmit = async (prompt) => {
    if (!prompt || isAgentRunning || !activeSessionId) return;
    
    setIsAgentRunning(true);
    setMessages(prev => [...prev, { type: 'user', text: prompt }]);

    try {
      await fetch('http://localhost:8000/agent/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_prompt: prompt,
          session_id: activeSessionId, // Pass the active session ID
          client_id: clientId
        })
      });
    } catch (error) {
      setMessages(prev => [...prev, { type: 'agent_error', text: error.message }]);
      setIsAgentRunning(false);
    }
  };

  const handleFileSelect = async (filePath) => {
    setActiveFilePath(filePath);
    // In a real app, you'd fetch file content from the backend here
    // For now, we'll just simulate content
    setActiveFileContent(`Content of ${filePath}`);
  };

  const toggleLayoutMode = () => {
    setLayoutMode(prevMode => (prevMode === 'simple' ? 'vscode' : 'simple'));
  };

  // --- RENDER ---
  return (
    <div className="container-fluid vh-100 p-0 d-flex flex-column">
      <Header />
      <div className="d-flex flex-grow-1">
        {/* Layout Mode Switch */}
        <div className="p-2 bg-light border-bottom">
          <button className="btn btn-sm btn-outline-secondary" onClick={toggleLayoutMode}>
            Switch to {layoutMode === 'simple' ? 'VS Code Layout' : 'Simple Layout'}
          </button>
        </div>

        {layoutMode === 'simple' ? (
          <div className="d-flex flex-grow-1">
            <div className="d-none d-md-flex flex-column col-md-3 col-lg-2 p-0">
              <SessionList sessions={sessions} activeSessionId={activeSessionId} onNewSession={handleNewSession} onSelectSession={handleSelectSession} />
            </div>

            <div className="offcanvas offcanvas-start d-md-none bg-body-tertiary" tabIndex="-1" id="session-sidebar">
              <div className="offcanvas-header">
                  <h5 className="offcanvas-title">Sessions</h5>
                  <button type="button" className="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
              </div>
              <div className="offcanvas-body p-0">
                  <SessionList sessions={sessions} activeSessionId={activeSessionId} onNewSession={handleNewSession} onSelectSession={handleSelectSession} />
              </div>
            </div>
            
            <main className="d-flex flex-column flex-grow-1 h-100">
              <div className="flex-grow-1" style={{ overflowY: 'auto' }}>
                <ChatLog messages={messages} />
              </div>
              <div>
                <InputBar onSubmit={handleAgentSubmit} isRunning={isAgentRunning} />
              </div>
            </main>
          </div>
        ) : (
          <PanelGroup direction="horizontal" className="d-flex flex-grow-1">
            <Panel defaultSize={20} minSize={10}>
              <div className="d-flex flex-column h-100 bg-light border-end">
                <h6 className="p-2 mb-0 border-bottom">Files</h6>
                {/* Placeholder for File Tree Component */}
                <div className="flex-grow-1 p-2" style={{ overflowY: 'auto' }}>
                  <p>File Tree will go here.</p>
                  <button onClick={() => handleFileSelect('src/App.jsx')}>Open App.jsx</button>
                </div>
              </div>
            </Panel>
            <PanelResizeHandle className="bg-secondary" style={{ width: '5px' }} />
            <Panel defaultSize={50} minSize={20}>
              <div className="d-flex flex-column h-100">
                <h6 className="p-2 mb-0 border-bottom">{activeFilePath || 'No file open'}</h6>
                <div className="flex-grow-1">
                  <Editor
                    height="100%"
                    language="javascript"
                    value={activeFileContent}
                    theme="vs-dark"
                    options={{
                      readOnly: true,
                      minimap: { enabled: false },
                      wordWrap: 'on',
                    }}
                  />
                </div>
              </div>
            </Panel>
            <PanelResizeHandle className="bg-secondary" style={{ width: '5px' }} />
            <Panel defaultSize={30} minSize={20}>
              <div className="d-flex flex-column h-100 bg-light border-start">
                <h6 className="p-2 mb-0 border-bottom">Chat</h6>
                <div className="flex-grow-1" style={{ overflowY: 'auto' }}>
                  <ChatLog messages={messages} />
                </div>
                <div>
                  <InputBar onSubmit={handleAgentSubmit} isRunning={isAgentRunning} />
                </div>
              </div>
            </Panel>
          </PanelGroup>
        )}
      </div>
    </div>
  );
}

export default App;

