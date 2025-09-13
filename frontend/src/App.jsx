import { useState, useEffect, useRef } from 'react';
import { useWebSocket } from './hooks/useWebSocket';
import SessionList from './components/SessionList';
import ChatLog from './components/ChatLog';
import InputBar from './components/InputBar';
import Header from './components/Header';
import FileTree from './components/FileTree';
import ToolStatus from './components/ToolStatus';
import { PanelGroup, Panel, PanelResizeHandle } from 'react-resizable-panels';
import Editor from '@monaco-editor/react';
import './App.css';
import './modern-theme.css';

function App() {
  const fileTreeRef = useRef(null);
  // --- STATE MANAGEMENT ---
  const [clientId] = useState(() => `client_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
  const [messages, setMessages] = useState([]);
  const [isAgentRunning, setIsAgentRunning] = useState(false);
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [layoutMode, setLayoutMode] = useState('simple'); // 'simple' or 'vscode'
  const [theme, setTheme] = useState('light'); // 'light' or 'dark'
  const [activeFileContent, setActiveFileContent] = useState('');
  const [activeFilePath, setActiveFilePath] = useState('');
  const [activeOperations, setActiveOperations] = useState([]); // Track active tool operations

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
      case 'tool_start':
        // Add operation to active operations list
        setActiveOperations(prev => [...prev, {
          id: lastMessage.data.id || Date.now(),
          type: lastMessage.data.tool_type,
          description: lastMessage.data.description,
          startTime: Date.now()
        }]);
        setMessages(prev => [...prev, { 
          type: 'operation_loading', 
          text: `${lastMessage.data.description}...` 
        }]);
        break;
      case 'tool_complete':
        // Remove operation from active operations and add result message
        setActiveOperations(prev => prev.filter(op => op.id !== lastMessage.data.id));
        setMessages(prev => {
          // Remove the loading message and add the result
          const filtered = prev.filter(msg => msg.type !== 'operation_loading' || 
            !msg.text.includes(lastMessage.data.description));
          return [...filtered, {
            type: `${lastMessage.data.tool_type}_operation`,
            text: lastMessage.data.result,
            metadata: {
              status: lastMessage.data.success ? 'success' : 'error',
              duration: lastMessage.data.duration
            }
          }];
        });
        break;
      case 'file_operation':
        if (fileTreeRef.current) {
          fileTreeRef.current.updateFileOperationStatus(lastMessage.data.path, lastMessage.data.operation);
          fileTreeRef.current.fetchFiles();
        }
        setMessages(prev => [...prev, {
          type: 'file_operation',
          text: lastMessage.data.result || lastMessage.data,
          metadata: {
            status: lastMessage.data.success !== false ? 'success' : 'error',
            operation: lastMessage.data.operation,
            path: lastMessage.data.path
          }
        }]);
        break;
      case 'terminal_output':
        setMessages(prev => [...prev, {
          type: 'terminal_operation',
          text: lastMessage.data.output || lastMessage.data,
          metadata: {
            status: lastMessage.data.exit_code === 0 ? 'success' : 'error',
            command: lastMessage.data.command,
            exitCode: lastMessage.data.exit_code
          }
        }]);
        break;
      case 'browser_action':
        setMessages(prev => [...prev, {
          type: 'browser_operation',
          text: lastMessage.data.result || lastMessage.data,
          metadata: {
            status: lastMessage.data.success !== false ? 'success' : 'error',
            action: lastMessage.data.action,
            url: lastMessage.data.url
          }
        }]);
        break;
      case 'finish':
        setMessages(prev => [...prev, { type: 'agent', text: lastMessage.data }]);
        setIsAgentRunning(false);
        setActiveOperations([]); // Clear any remaining operations
        break;
      case 'error':
        setMessages(prev => [...prev, { type: 'agent_error', text: lastMessage.data }]);
        setIsAgentRunning(false);
        setActiveOperations([]); // Clear any remaining operations
        break;
    }
  }, [lastMessage]);

  // --- SESSION DATA FETCHING ---
  
  // Effect to fetch all sessions on initial app load
  useEffect(() => {
    const fetchSessions = async () => {
      try {
        const response = await fetch('https://ethcobackend.onrender.com/sessions');
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
            const response = await fetch(`https://ethcobackend.onrender.com/sessions/${activeSessionId}`);
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
        const response = await fetch('https://ethcobackend.onrender.com/sessions', { method: 'POST' });
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
      await fetch('https://ethcobackend.onrender.com/agent/run', {
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
    try {
      const response = await fetch(`https://ethcobackend.onrender.com/sessions/${activeSessionId}/file_content?path=${filePath}`);
      if (!response.ok) throw new Error("Failed to fetch file content");
      const data = await response.json();
      if (data.status === "error") {
        throw new Error(data.message);
      }
      setActiveFileContent(data.content);
    } catch (error) {
      console.error("Error fetching file content:", error);
      setActiveFileContent(`Error loading file: ${error.message}`);
    }
  };

  const handleSaveFile = async () => {
    if (!activeFilePath) return;

    try {
      const response = await fetch(`https://ethcobackend.onrender.com/sessions/${activeSessionId}/files`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          path: activeFilePath,
          content: activeFileContent,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to save file');
      }

      const result = await response.json();
      if (result.status === 'error') {
        throw new Error(result.message);
      }

      // Optionally, show a success message
      console.log('File saved successfully');

    } catch (error) {
      console.error('Error saving file:', error);
      // Optionally, show an error message to the user
    }
  };

  const toggleLayoutMode = () => {
    setLayoutMode(prevMode => (prevMode === 'simple' ? 'vscode' : 'simple'));
  };

  const toggleTheme = () => {
    setTheme(prevTheme => (prevTheme === 'light' ? 'dark' : 'light'));
  };

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  // --- RENDER ---
  return (
    <div className="app-container">
      <Header toggleTheme={toggleTheme} theme={theme} />
      <div className="d-flex flex-grow-1">
        {/* Layout Mode Switch */}
        <div className="p-2 bg-light border-bottom">
          <button className="layout-toggle" onClick={toggleLayoutMode}>
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
                <div className="flex-grow-1 p-2" style={{ overflowY: 'auto' }}>
                  <FileTree ref={fileTreeRef} sessionId={activeSessionId} onFileSelect={handleFileSelect} />
                </div>
              </div>
            </Panel>
            <PanelResizeHandle className="bg-secondary" style={{ width: '5px' }} />
            <Panel defaultSize={50} minSize={20}>
              <div className="d-flex flex-column h-100">
                <h6 className="p-2 mb-0 border-bottom">{activeFilePath || 'No file open'}
                  {activeFilePath && <button onClick={handleSaveFile}>Save</button>}
                </h6>
                <div className="flex-grow-1">
                  <Editor
                    height="100%"
                    language="javascript"
                    value={activeFileContent}
                    theme="vs-dark"
                    onChange={(value) => setActiveFileContent(value)}
                    options={{
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
      
      {/* Tool Status Component for real-time feedback */}
      <ToolStatus activeOperations={activeOperations} />
    </div>
  );
}

export default App;

