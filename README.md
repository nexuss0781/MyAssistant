# Ethco AI - Advanced Autonomous Agent

Ethco AI is a sophisticated autonomous AI agent built with a React frontend and Python FastAPI backend. It features a VS Code-inspired interface, comprehensive tool integration, and advanced memory management capabilities for enhanced productivity and development workflows.

## 🚀 Key Features

### VS Code-Inspired Interface
- **Dual Layout Modes**: Switch between simple chat interface and professional VS Code-inspired layout
- **Three-Pane Layout**: File Tree (left), Monaco Code Editor (center), Chat Window (right)
- **Resizable Panels**: Customizable workspace with drag-to-resize functionality
- **Monaco Editor Integration**: Full-featured code editor with syntax highlighting and IntelliSense

### Advanced AI Capabilities
- **Autonomous Task Execution**: AI agent can plan, execute, and complete complex multi-step tasks
- **Real-time Progress Tracking**: Live updates on task progress with visual indicators
- **Memory Management**: Persistent knowledge storage and context-aware conversations
- **Session Management**: Multiple concurrent sessions with isolated workspaces

### Comprehensive Tool Integration
- **Filesystem Operations**: Complete file and folder management within sandboxed environments
- **Terminal Execution**: Execute arbitrary shell commands with real-time output capture
- **Browser Automation**: Web navigation, content extraction, and element interaction
- **Memory System**: Advanced knowledge storage, retrieval, and persona management

### Real-time Communication
- **WebSocket Integration**: Live bidirectional communication between frontend and backend
- **Progress Indicators**: Visual feedback for ongoing operations
- **Error Handling**: Comprehensive error reporting and recovery mechanisms

## 🏗️ Project Structure

```
MyAssistant/
├── backend/                    # Python FastAPI backend
│   ├── app/                   # Core application logic
│   │   ├── agent_core.py      # Main agent execution engine
│   │   ├── gemini_handler.py  # Gemini API integration
│   │   ├── filesystem_tools.py # File system operations
│   │   ├── terminal_tools.py   # Terminal command execution
│   │   ├── browser_tools.py    # Web browser automation
│   │   ├── memory_manager.py   # Advanced memory management
│   │   ├── session_manager.py  # Session handling
│   │   ├── websocket_manager.py # Real-time communication
│   │   └── main.py            # FastAPI application entry point
│   ├── sessions/              # Session-specific workspaces
│   ├── memory/                # Persistent memory storage
│   ├── prompt.md              # AI agent constitution and directives
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile            # Backend containerization
├── frontend/                  # React frontend application
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── ChatLog.jsx    # Chat interface
│   │   │   ├── FileTree.jsx   # File explorer
│   │   │   ├── Header.jsx     # Application header
│   │   │   ├── InputBar.jsx   # User input interface
│   │   │   ├── Message.jsx    # Message display
│   │   │   ├── SessionList.jsx # Session management
│   │   │   └── TaskProgress.jsx # Task progress tracking
│   │   ├── hooks/
│   │   │   └── useWebSocket.js # WebSocket hook
│   │   ├── App.jsx            # Main application component
│   │   └── main.jsx           # Application entry point
│   ├── package.json           # Frontend dependencies
│   ├── vite.config.js         # Vite configuration
│   └── Dockerfile            # Frontend containerization
├── docker-compose.yml         # Multi-container orchestration
├── TODO.md                    # Development roadmap
├── DEPLOYMENT.md              # Deployment instructions
└── README.md                  # This file
```

## 🛠️ Setup and Installation

### Prerequisites

- **Node.js** (v18 or higher) with npm
- **Python** 3.11 or higher
- **Git** for version control
- **Docker** (optional, for containerized deployment)

### Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/nexuss0781/MyAssistant.git
   cd MyAssistant
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   pip install python-dotenv uvicorn
   ```

3. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Environment Configuration**
   Create a `.env` file in the backend directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ENVIRONMENT=development
   ```

### Running the Application

#### Development Mode

1. **Start the Backend Server**
   ```bash
   cd backend
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   Backend accessible at: `http://localhost:8000`

2. **Start the Frontend Development Server**
   ```bash
   cd frontend
   npm run dev
   ```
   Frontend accessible at: `http://localhost:5173`

#### Production Mode with Docker

```bash
docker-compose up -d
```

## 🎯 Usage Guide

### Getting Started

1. **Access the Application**: Navigate to `http://localhost:5173` in your web browser
2. **Choose Layout Mode**: Toggle between Simple and VS Code layouts using the layout switch button
3. **Create a Session**: Start a new session or select an existing one from the session list
4. **Interact with the Agent**: Type your requests in the chat input and watch the agent execute tasks

### VS Code Layout Features

#### File Tree Panel
- Browse project files and directories
- Click on files to open them in the Monaco Editor
- Real-time updates when the agent modifies files

#### Monaco Editor Panel
- Full-featured code editor with syntax highlighting
- Support for multiple programming languages
- Read-only mode for viewing agent-generated content
- Line numbers, minimap, and word wrap options

#### Chat Panel
- Real-time conversation with the AI agent
- Task progress tracking with visual indicators
- Error reporting and status updates
- Command input with execution feedback

### Agent Capabilities

#### Filesystem Operations
```
- Create, read, update, and delete files and folders
- Navigate directory structures
- File content manipulation and editing
- Workspace isolation per session
```

#### Terminal Execution
```
- Execute shell commands with real-time output
- Interactive command support
- Working directory management
- Command history and error handling
```

#### Browser Automation
```
- Navigate to web pages
- Extract content (text, HTML, markdown)
- Interact with web elements
- Take screenshots
- Web search capabilities
```

#### Memory Management
```
- Persistent knowledge storage
- Context-aware conversations
- User preference tracking
- Adaptive persona development
```

## 🔧 API Documentation

### Backend Endpoints

#### Session Management
- `GET /sessions` - List all sessions
- `POST /sessions` - Create new session
- `GET /sessions/{session_id}` - Get session history
- `GET /sessions/{session_id}/files` - Get file tree
- `GET /sessions/{session_id}/file_content` - Get file content

#### Agent Operations
- `POST /agent/run` - Execute agent task
- `GET /health` - Health check endpoint

#### WebSocket Endpoints
- `WS /ws/{client_id}` - Real-time communication

### Frontend Components

#### Core Components
- **App.jsx**: Main application with layout management
- **ChatLog.jsx**: Message display and conversation history
- **FileTree.jsx**: File explorer with hierarchical display
- **InputBar.jsx**: User input interface with submission handling

#### Hooks
- **useWebSocket.js**: WebSocket connection management and message handling

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

### Integration Testing
```bash
# Start both backend and frontend
# Run end-to-end tests
npm run test:e2e
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Scale services
docker-compose up -d --scale backend=2
```

### Manual Deployment

#### Backend Deployment
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Frontend Deployment
```bash
cd frontend
npm run build
# Serve the dist/ directory with your preferred web server
```

## 🔒 Security Considerations

- **Sandboxed Execution**: All file operations are contained within session-specific directories
- **Input Validation**: Comprehensive validation of user inputs and API requests
- **Error Handling**: Secure error messages that don't expose system information
- **Session Isolation**: Each session operates in an isolated workspace

## 🤝 Contributing

We welcome contributions to Ethco AI! Please follow these guidelines:

1. **Fork the Repository**: Create your own fork of the project
2. **Create a Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Make Changes**: Implement your feature or bug fix
4. **Add Tests**: Ensure your changes are covered by tests
5. **Commit Changes**: `git commit -m 'Add amazing feature'`
6. **Push to Branch**: `git push origin feature/amazing-feature`
7. **Open Pull Request**: Submit your changes for review

### Development Guidelines

- Follow existing code style and conventions
- Add comprehensive tests for new features
- Update documentation for any API changes
- Ensure all tests pass before submitting

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini API** for advanced language model capabilities
- **Monaco Editor** for the professional code editing experience
- **React Resizable Panels** for the flexible layout system
- **FastAPI** for the high-performance backend framework
- **Playwright** for browser automation capabilities

## 📞 Support

For support, questions, or feature requests:

- **Issues**: [GitHub Issues](https://github.com/nexuss0781/MyAssistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/nexuss0781/MyAssistant/discussions)
- **Documentation**: [Project Wiki](https://github.com/nexuss0781/MyAssistant/wiki)

---

**Ethco AI** - Empowering developers with intelligent automation and professional-grade tools for enhanced productivity and seamless development workflows.

