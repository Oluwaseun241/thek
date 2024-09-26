# Thek

`Thek` is a Backend API for managing books in a library. It allows administrators
to perform operations such as adding new books, removing books, and managing user data.
It also communicates with a separate Frontend API using RabbitMQ to notify it of changes
(e.g., when a book is added or removed). The backend leverages MongoDB for storing data
and is containerized using Docker for easy deployment.

## Features

- **Books Management**:

  - Add new books to the library catalogue.
  - Remove books from the library catalogue.
  - List all books in the library.

- **User Management**:

  - List all users enrolled in the library.

- **RabbitMQ Integration**:

  - Sends notifications when books are added or removed so the **Frontend API** can update its catalogue.

- **MongoDB**:
  - Store and retrieve data related to books and users.

---

## **Technology Stack**

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) - High-performance Python web framework.
- **Database**: [MongoDB](https://www.mongodb.com/) - NoSQL database used for storing user and book data.
- **Messaging Queue**: [RabbitMQ](https://www.rabbitmq.com/) - For communicating book catalogue changes to the Frontend API.
- **Containerization**: [Docker](https://www.docker.com/) - For running the app in isolated containers.
- **Testing**: [pytest](https://pytest.org/) - For unit and integration tests.

---

## Running the Application

```
docker-compose up --build
```

- This will build and run the Both APIs, MongoDB, and RabbitMQ services in separate containers.

- The Frontend API will be accessible at http://localhost:8000 while
  Backend at http://localhost:8001.
