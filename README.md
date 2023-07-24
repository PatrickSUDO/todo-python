# Todo App

A simple Todo application written in Python using FastAPI and PostgreSQL.

## Prerequisites

- Docker
- Docker Compose

## Starting the Application

To start the application, use the following command in the terminal:

```bash
docker-compose up app
```

This will start the application and the PostgreSQL database in separate Docker containers. The application will be accessible at `http://localhost:8000`.

## API Documentation

Once the application is running, you can view the Swagger UI for the API documentation and to test the API endpoints. It is accessible at `http://localhost:8000/docs`.

## Running Tests

To run the unit tests, use the following command in the terminal:

```bash
docker-compose up test
```

This will start a separate instance of the PostgreSQL database for testing, run the tests in a Docker container, and then stop the database.


