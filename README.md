# Ethco AI - Autonomous AI Agent Development Environment

Ethco AI is a sophisticated autonomous AI agent development environment featuring a VS Code-inspired interface with real-time tool usage feedback, comprehensive file management, terminal execution, and browser integration capabilities.

## 🚀 Features

### Core Capabilities
- **🤖 Autonomous AI Agent**: Powered by Google Gemini for intelligent task planning and execution
- **📁 Advanced File Management**: Hierarchical file tree with folder expansion and file type icons
- **💻 Terminal Integration**: Execute shell commands with real-time output display
- **🌐 Browser Automation**: Web navigation, content extraction, and element interaction using Playwright
- **🧠 Memory Management**: Persistent knowledge storage and persona adaptation
- **⚡ Real-time Feedback**: Visual indicators for all tool operations and progress tracking

### User Interface
- **🎨 Professional Styling**: Modern, responsive design with professional theming
- **🔄 Dual Layout Modes**: Switch between simple chat interface and VS Code-inspired layout
- **📝 Monaco Editor Integration**: Full-featured code editor with syntax highlighting
- **💬 Enhanced Chat Experience**: Rich message types with operation status indicators
- **📊 Task Progress Tracking**: Visual task completion with real-time updates

### Technical Features
- **🔗 WebSocket Communication**: Real-time bidirectional communication
- **📦 Session Management**: Persistent session history and workspace isolation
- **🛠️ Comprehensive Tool Suite**: File operations, terminal commands, browser actions, and memory management
- **🔧 Modular Architecture**: Clean separation between frontend and backend components

## 🏗️ Architecture

### Backend (Python FastAPI)
- **Agent Core** (`agent_core.py`): Main orchestration and plan execution
- **Tool Modules**: 
  - `filesystem_tools.py`: File and directory operations
  - `terminal_tools.py`: Shell command execution
  - `browser_tools.py`: Web automation with Playwright
  - `memory_manager.py`: Persistent knowledge and persona management
- **Communication**: WebSocket manager for real-time updates
- **AI Integration**: Gemini handler for plan generation

### Frontend (React + Vite)
- **Modern React**: Functional components with hooks
- **Resizable Panels**: VS Code-like layout with `react-resizable-panels`
- **Monaco Editor**: Full-featured code editor integration
- **Real-time UI**: WebSocket-powered live updates
- **Professional Styling**: CSS custom properties and responsive design

## 📋 Prerequisites

- **Node.js** (v18 or higher) with npm
- **Python** (v3.11 or higher)
- **Git** for version control

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ethco-ai
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
```

### 4. Environment Configuration
Create a `.env` file in the backend directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## 🚀 Running the Application

### Development Mode

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Access the application:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Production Build

**Frontend:**
```bash
cd frontend
npm run build
```

**Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🎯 Usage Guide

### Getting Started
1. **Open the Application**: Navigate to http://localhost:5173
2. **Choose Layout**: Toggle between Simple and VS Code layouts
3. **Start a Session**: Create a new session or select an existing one
4. **Interact with AI**: Send prompts to the AI agent in the chat interface

### Layout Modes

#### Simple Layout
- Clean chat interface
- Session list sidebar
- Perfect for conversational interactions

#### VS Code Layout
- **Left Panel**: Hierarchical file tree with folder expansion
- **Center Panel**: Monaco code editor with syntax highlighting
- **Right Panel**: Chat interface with real-time feedback
- **Resizable panels** for optimal workspace organization

### AI Agent Capabilities

The AI agent can perform various tasks through natural language commands:

#### File Operations
- Create, read, update, and delete files and folders
- Navigate directory structures
- Display file contents in the Monaco editor

#### Terminal Commands
- Execute shell commands with real-time output
- Support for complex command chains
- Error handling and exit code reporting

#### Browser Automation
- Navigate to websites
- Extract content (text, HTML, markdown)
- Interact with web elements
- Take screenshots
- Perform web searches

#### Memory Management
- Store and retrieve knowledge across sessions
- Adapt persona based on interactions
- Maintain context and preferences

### Visual Feedback System

The application provides comprehensive visual feedback:
- **🔵 File Operations**: Blue indicators for file/folder actions
- **🟢 Terminal Commands**: Green indicators for shell execution
- **🟡 Browser Actions**: Yellow indicators for web automation
- **⚪ Memory Operations**: Gray indicators for knowledge management
- **📊 Progress Bars**: Real-time operation progress
- **✅ Success/❌ Error States**: Clear status indication

## 🔧 Configuration

### Backend Configuration
- **Session Storage**: Sessions are stored in `backend/sessions/`
- **File Operations**: Sandboxed within session directories
- **WebSocket**: Real-time communication on `/ws/{client_id}`
- **CORS**: Configured for frontend development server

### Frontend Configuration
- **Development Server**: Vite with hot module replacement
- **WebSocket Connection**: Automatic reconnection handling
- **Theme System**: CSS custom properties for easy customization
- **Responsive Design**: Mobile-friendly interface

## 🧪 Testing

### Frontend Testing
```bash
cd frontend
npm run lint          # ESLint checks
npm run build         # Production build test
```

### Backend Testing
```bash
cd backend
source venv/bin/activate
python -c "import app.main; print('Backend imports successfully')"
```

## 📁 Project Structure

```
ethco-ai/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── agent_core.py        # Agent orchestration
│   │   ├── filesystem_tools.py  # File operations
│   │   ├── terminal_tools.py    # Shell commands
│   │   ├── browser_tools.py     # Web automation
│   │   ├── memory_manager.py    # Knowledge storage
│   │   ├── session_manager.py   # Session handling
│   │   ├── websocket_manager.py # Real-time communication
│   │   └── gemini_handler.py    # AI integration
│   ├── requirements.txt         # Python dependencies
│   ├── prompt.md               # AI agent constitution
│   ├── sessions/               # Session workspaces
│   └── venv/                   # Virtual environment
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── hooks/             # Custom hooks
│   │   ├── App.jsx            # Main application
│   │   ├── App.css            # Professional styling
│   │   └── index.css          # Base styles
│   ├── package.json           # Node dependencies
│   └── dist/                  # Production build
├── TODO.md                    # Implementation roadmap
├── README.md                  # This file
└── docker-compose.yml         # Container orchestration
```

## 🤝 Contributing

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Commit Changes**: `git commit -m 'Add amazing feature'`
4. **Push to Branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### Development Guidelines
- Follow existing code style and conventions
- Add comments for complex logic
- Test thoroughly before submitting
- Update documentation as needed

## 🐛 Troubleshooting

### Common Issues

**Backend won't start:**
- Ensure virtual environment is activated
- Check Python version (3.11+ required)
- Verify all dependencies are installed

**Frontend build fails:**
- Clear node_modules: `rm -rf node_modules && npm install`
- Check Node.js version (18+ required)
- Ensure all dependencies are compatible

**WebSocket connection issues:**
- Check backend is running on port 8000
- Verify CORS configuration
- Check browser console for connection errors

**Playwright browser issues:**
- Run `playwright install chromium`
- Check system dependencies for headless browser support

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google Gemini** for AI capabilities
- **Playwright** for browser automation
- **Monaco Editor** for code editing
- **React** and **FastAPI** for the application framework
- **Bootstrap** for UI components

---

**Ethco AI** - Empowering autonomous AI development with professional tools and real-time feedback.