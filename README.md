# MyAssistant Project

This project is an AI Agent with a React frontend and a Python FastAPI backend. It allows users to interact with an AI agent that can perform various tasks, including file system operations.

## Project Structure

- `backend/`: Contains the Python FastAPI application.
  - `app/`: Core application logic, including agent core, Gemini handler, filesystem tools, session manager, and websocket manager.
  - `prompt.md`: The constitution/system prompt for the AI agent.
  - `requirements.txt`: Python dependencies for the backend.
  - `sessions/`: Directory for storing session-specific data and workspaces.
- `frontend/`: Contains the React application.
  - `public/`: Static assets.
  - `src/`: React source code.
  - `package.json`: Frontend dependencies and scripts.

## Setup and Running the Application

### Prerequisites

- Node.js (with npm)
- Python 3.11

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/nexuss0781/MyAssistant.git
    cd MyAssistant
    ```

2.  **Backend Setup:**
    ```bash
    cd backend
    pip install -r requirements.txt
    pip install python-dotenv uvicorn
    ```

3.  **Frontend Setup:**
    ```bash
    cd ../frontend
    npm install
    ```

### Running the Application

1.  **Start the Backend Server:**
    Open a new terminal, navigate to the `backend` directory, and run:
    ```bash
    cd backend
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```
    The backend will be accessible at `http://localhost:8000`.

2.  **Start the Frontend Development Server:**
    Open another terminal, navigate to the `frontend` directory, and run:
    ```bash
    cd frontend
    npm run dev
    ```
    The frontend will be accessible at `http://localhost:5173`.

## Key Features

-   **AI Agent Core:** Manages the agent's task execution, plan generation, and tool execution.
-   **Gemini Integration:** Utilizes the Gemini API for generating agent plans and responses.
-   **Filesystem Tools:** Allows the agent to interact with a sandboxed filesystem for each session.
-   **Session Management:** Handles the creation, retrieval, and history tracking of user sessions.
-   **WebSocket Communication:** Enables real-time communication between the frontend and backend for live updates on agent progress.
-   **Responsive Frontend:** Built with React, providing an interactive user interface.

## Debugging

-   **Backend:** The backend runs with `uvicorn`, which provides detailed logs in the terminal. You can also add `print()` statements in the Python code for debugging purposes.
-   **Frontend:** Use your browser's developer console to inspect React components, network requests, and console logs.

## Contributing

Feel free to fork the repository, make changes, and submit pull requests. Please ensure your code adheres to the existing style and passes all tests.

## License

[Specify your license here, e.g., MIT License]



## Frontend Configuration Update

During development, it was necessary to modify the `vite.config.js` file to allow the frontend development server to be accessible from outside `localhost`. The `server.allowedHosts` property was updated to include `.manus.computer`.

```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    strictPort: true,
    hmr: {
      port: 5173,
    },
    watch: {
      usePolling: true,
    },
    allowedHosts: [
      ".manus.computer"
    ]
  }
})
```


