# Installation Guide

This guide will walk you through the steps to install and run the frontend and backend of this project.

## Backend Installation

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```

3.  **Activate the virtual environment:**
    ```bash
    source .venv/bin/activate
    ```

4.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Install missing dependencies:**
    It seems that `requests` and `python-dotenv` are not listed in the `requirements.txt` file. You will need to install them manually.
    ```bash
    pip install requests python-dotenv
    ```

6.  **Run the backend server:**
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```
    The backend server should now be running on `http://0.0.0.0:8000`.

## Frontend Installation

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install the required dependencies:**
    ```bash
    npm install
    ```

3.  **Run the frontend development server:**
    ```bash
    npm run dev
    ```
    The frontend should now be running on `http://localhost:5173`.
