# AI Assistant Agent Platform

A powerful, full-stack AI agent platform that combines a React frontend with a Python FastAPI backend to create an intelligent assistant capable of performing complex tasks autonomously. The platform features real-time communication, session management, and a comprehensive toolkit for file operations, web browsing, terminal commands, and persistent memory management.

## 🚀 Key Features Overview

### 🤖 **Intelligent Agent Core**
- **AI-Powered Task Planning**: Generates structured execution plans using Google Gemini API
- **Autonomous Task Execution**: Breaks down complex requests into actionable steps
- **Real-time Progress Tracking**: Live updates on task execution status
- **Error Handling & Recovery**: Robust error management with graceful fallbacks

### 💬 **Interactive Chat Interface**
- **Real-time Communication**: WebSocket-based instant messaging
- **Session Management**: Persistent conversation history across sessions
- **Task Progress Visualization**: Visual indicators for completed and pending tasks
- **Responsive Design**: Mobile-friendly interface with Bootstrap styling

### 🗂️ **File System Operations**
- **File Management**: Create, read, update, and delete files and folders
- **Content Manipulation**: Add content to files with syntax highlighting support
- **Directory Navigation**: Browse and explore file structures
- **Session-Isolated Workspaces**: Each session has its own sandboxed file system

### 🌐 **Web Browsing Capabilities**
- **URL Navigation**: Navigate to any web page programmatically
- **Content Extraction**: Extract text and HTML content from web pages
- **Web Search**: Perform web searches and retrieve results
- **Element Interaction**: Click, type, and interact with web page elements
- **Screenshot Capture**: Take screenshots of web pages
- **Headless Browser Integration**: Powered by Playwright for reliable web automation

### 💻 **Terminal Command Execution**
- **Shell Command Execution**: Run any terminal command with timeout protection
- **Output Capture**: Capture both stdout and stderr from executed commands
- **Cross-Platform Support**: Works on Linux, macOS, and Windows environments
- **Secure Execution**: Sandboxed command execution within session context

### 🧠 **Persistent Memory Management**
- **Knowledge Storage**: Save and retrieve key-value pairs for long-term memory
- **Persona Management**: Maintain and update AI persona characteristics
- **Session-Specific Memory**: Each session maintains its own memory space
- **JSON-Based Storage**: Structured data storage with atomic file operations

### 🔧 **Advanced UI Features**
- **Dual Layout Modes**: Simple chat interface and VS Code-like layout
- **File Tree Explorer**: Navigate session files with expandable tree structure
- **Code Editor Integration**: Monaco Editor for viewing and editing files
- **Resizable Panels**: Customizable workspace layout with drag-to-resize panels
- **Session Switching**: Easy switching between multiple conversation sessions

## 🏗️ Architecture

### Frontend (React + Vite)
- **Modern React**: Built with React 19 and modern hooks
- **Real-time Updates**: WebSocket integration for live communication
- **Responsive Design**: Bootstrap 5 for mobile-first responsive design
- **Code Editing**: Monaco Editor integration for syntax-highlighted code viewing
- **Component Architecture**: Modular components for maintainable code

### Backend (FastAPI + Python)
- **High-Performance API**: FastAPI with async/await support
- **WebSocket Manager**: Real-time bidirectional communication
- **Session Management**: Persistent session storage and history tracking
- **Tool Integration**: Modular tool system for extensible functionality
- **Error Handling**: Comprehensive error handling and logging

## 🛠️ End-to-End Feature Workflows

### 1. **Intelligent Task Execution**
```
User Input → Plan Generation → Task Parsing → Tool Execution → Real-time Updates → Completion
```
- User submits a natural language request
- AI generates a structured execution plan
- Plan is parsed into executable commands
- Tools are executed sequentially with progress updates
- Results are displayed in real-time to the user

### 2. **File System Management**
```
Request → File Operations → Session Storage → UI Updates → Persistence
```
- Create, modify, and organize files and folders
- All operations are scoped to individual sessions
- Changes are immediately reflected in the file tree UI
- File contents can be viewed in the integrated code editor

### 3. **Web Automation Workflow**
```
URL/Search → Browser Navigation → Content Extraction → Element Interaction → Screenshot/Data
```
- Navigate to websites or perform web searches
- Extract content in various formats (text, HTML, structured data)
- Interact with page elements (click, type, scroll)
- Capture screenshots for visual verification

### 4. **Terminal Integration**
```
Command Input → Secure Execution → Output Capture → Result Display → History Logging
```
- Execute shell commands with timeout protection
- Capture and display command output in real-time
- Maintain command history within session context
- Support for complex command chains and scripts

### 5. **Memory and Learning**
```
Information → Knowledge Extraction → Storage → Retrieval → Context Application
```
- Extract and store important information during conversations
- Maintain persistent memory across sessions
- Retrieve relevant context for future interactions
- Update and evolve AI persona based on interactions

## 📋 Installation & Setup

### Prerequisites
- **Node.js** (v18 or higher) with npm
- **Python** 3.11 or higher
- **Docker** (optional, for containerized deployment)

### Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd ai-assistant-platform
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
   - Create `.env` file in the backend directory
   - Add required API keys and configuration variables

### Running the Application

1. **Start Backend Server**
   ```bash
   cd backend
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   Backend will be available at `http://localhost:8000`

2. **Start Frontend Development Server**
   ```bash
   cd frontend
   npm run dev
   ```
   Frontend will be available at `http://localhost:5173`

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access the application
# Frontend: http://localhost:80
# Backend API: http://localhost:8000
```

## 🎯 Use Cases

### **Development Assistant**
- Generate and modify code files
- Execute build commands and tests
- Browse documentation and Stack Overflow
- Manage project structure and dependencies

### **Research and Analysis**
- Search the web for information
- Extract and summarize content from websites
- Store findings in persistent memory
- Generate reports and documentation

### **System Administration**
- Execute system commands and scripts
- Monitor file systems and processes
- Automate routine maintenance tasks
- Generate system reports and logs

### **Content Creation**
- Create and organize content files
- Research topics through web browsing
- Generate structured documents
- Maintain knowledge bases and wikis

## 🔌 API Endpoints

### Session Management
- `GET /sessions` - List all sessions
- `POST /sessions` - Create new session
- `GET /sessions/{session_id}` - Get session history

### Agent Operations
- `POST /agent/run` - Execute agent task
- `WebSocket /ws/{client_id}` - Real-time communication

### File System
- `GET /sessions/{session_id}/files` - List session files
- `GET /sessions/{session_id}/file_content` - Get file content

### Health Check
- `GET /health` - Service health status

## 🔧 Configuration

### Frontend Configuration (vite.config.js)
```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    strictPort: true,
    hmr: { port: 5173 },
    watch: { usePolling: true }
  }
})
```

### Backend Configuration
- CORS origins configuration for cross-origin requests
- WebSocket connection management
- Session storage directory configuration
- API timeout and rate limiting settings

## 🛡️ Security Features

- **Session Isolation**: Each session operates in its own sandboxed environment
- **Command Timeout Protection**: Prevents long-running or hanging commands
- **Input Validation**: Comprehensive input sanitization and validation
- **CORS Configuration**: Controlled cross-origin resource sharing
- **Error Boundaries**: Graceful error handling without system crashes

## 📊 Monitoring and Logging

- **Structured Logging**: Comprehensive logging across all components
- **Real-time Status Updates**: Live progress tracking through WebSocket
- **Error Reporting**: Detailed error messages and stack traces
- **Performance Monitoring**: Request/response timing and resource usage

## 🔄 Development Workflow

1. **Feature Development**: Add new tools and capabilities to the agent
2. **Testing**: Comprehensive testing of individual components and workflows
3. **Integration**: Seamless integration of new features with existing system
4. **Deployment**: Docker-based deployment for consistent environments
5. **Monitoring**: Real-time monitoring and logging for production systems

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes with appropriate tests
4. Submit a pull request with detailed description
5. Ensure all tests pass and code follows style guidelines

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, bug reports, or feature requests:
- Create an issue in the GitHub repository
- Check the documentation and API reference
- Review existing issues and discussions

---

**Built with ❤️ using React, FastAPI, and modern web technologies**