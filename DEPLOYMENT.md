# Deployment Guide

This guide provides instructions on how to deploy the MyAssistant application using Docker and Docker Compose.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

-   **Docker:** [Install Docker Engine](https://docs.docker.com/engine/install/)
-   **Docker Compose:** [Install Docker Compose](https://docs.docker.com/compose/install/)

## Deployment Steps

1.  **Clone the Repository:**

    If you haven't already, clone the MyAssistant repository to your local machine:

    ```bash
    git clone https://github.com/nexuss0781/MyAssistant.git
    cd MyAssistant
    ```

2.  **Build and Run with Docker Compose:**

    Navigate to the root directory of the cloned repository (where `docker-compose.yml` is located) and run the following command:

    ```bash
    docker compose up --build -d
    ```

    -   `docker compose up`: This command starts the services defined in your `docker-compose.yml` file.
    -   `--build`: This flag tells Docker Compose to build the images for your services before starting the containers. This is necessary when you make changes to your Dockerfiles or application code.
    -   `-d`: This flag runs the containers in detached mode, meaning they will run in the background and not tie up your terminal.

3.  **Access the Application:**

    Once the containers are up and running:

    -   **Frontend:** The frontend application will be accessible in your web browser at `http://localhost` (port 80 is mapped from the container's port 80).
    -   **Backend:** The backend API will be accessible at `http://localhost:8000` (port 8000 is mapped from the container's port 8000).

## Stopping the Application

To stop the running containers, navigate to the root directory of the repository and execute:

```bash
docker compose down
```

This command will stop and remove the containers, networks, and volumes created by `docker compose up`.

## Troubleshooting

-   **Port Conflicts:** If you encounter issues with ports already being in use, ensure no other applications are running on ports 80 or 8000 on your host machine.
-   **Container Logs:** To view the logs of a specific service for debugging, use:
    ```bash
    docker compose logs <service_name>
    ```
    Replace `<service_name>` with `frontend` or `backend`.


