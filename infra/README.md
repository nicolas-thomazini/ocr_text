# Infrastructure (Docker) Overview

This directory and the root docker-compose.yml orchestrate the Family Search OCR project using Docker.

## Structure

- `backend/Dockerfile`: Builds the FastAPI backend container
- `frontend/Dockerfile`: Builds the React/Vite frontend container
- `docker-compose.yml`: Orchestrates backend, frontend, and PostgreSQL database

## Usage

- To build and run all services:
  ```bash
  docker-compose up --build
  ```
- To stop all services:
  ```bash
  docker-compose down
  ```

## Notes
- Environment variables for each service can be set in the compose file or via `.env` files
- Volumes are used for database persistence and code hot-reload (dev)
- Adjust ports and variables as needed for your environment 