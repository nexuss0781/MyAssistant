# AI Agent Project

This project is a web-based AI agent that can perform various tasks. It consists of a React frontend and a Python backend.

## Setup and Usage

### Prerequisites

- Node.js and npm
- Python 3.11

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd ai-agent-project
   ```

2. **Frontend:**
   ```bash
   cd frontend
   npm install
   ```

3. **Backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the backend server:**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. **Start the frontend development server:**
   ```bash
   cd frontend
   npm run dev
   ```

## GitHub Actions

This project uses GitHub Actions to automate the build and test processes. The workflow is defined in `.github/workflows/ci.yml`.