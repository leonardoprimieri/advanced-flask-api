# Advanced Flask API

A secure Flask REST API with user authentication, role-based access control, and MySQL database integration. Features user management, secure password hashing, and session management.

## Features

- **User Authentication**: Login/logout with secure session management
- **Password Security**: BCrypt hashing for secure password storage
- **Role-Based Access Control**: Admin and user roles with different permissions
- **RESTful API**: Clean REST endpoints for user operations
- **Database Integration**: MySQL database with SQLAlchemy ORM
- **Containerized Database**: Docker Compose for easy MySQL setup

## Tech Stack

- **Backend**: Flask 2.3.0
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: Flask-Login with session management
- **Security**: BCrypt password hashing
- **Containerization**: Docker Compose for database

## Project Structure

```
advanced-flask-api/
├── app.py              # Main Flask application
├── database.py         # Database configuration
├── models/
│   └── user.py        # User model
├── requirements.txt    # Python dependencies
├── docker-compose.yaml # MySQL container setup
└── README.md          # Project documentation
```

## API Endpoints

### Authentication

#### Login

- **POST** `/login`
- **Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**: `200` - Success, `400` - Invalid credentials

#### Logout

- **GET** `/logout`
- **Auth**: Required
- **Response**: `200` - User logged out

### User Management

#### Create User

- **POST** `/user`
- **Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**: `200` - User created, `400` - Missing data/User exists

#### Get User

- **GET** `/user/<user_id>`
- **Auth**: Required
- **Response**: `200` - User data, `404` - User not found

#### Update Password

- **PUT** `/user/update-password/<user_id>`
- **Auth**: Required (own account or admin)
- **Body**:
  ```json
  {
    "password": "string"
  }
  ```
- **Response**: `200` - Success, `401` - Unauthorized, `403` - Missing password, `404` - User not found

#### Delete User

- **DELETE** `/user/<user_id>`
- **Auth**: Required (admin only)
- **Response**: `200` - User deleted, `401` - Unauthorized, `404` - User not found, `409` - Cannot delete self

## Security Features

- **Password Hashing**: BCrypt with salt for secure password storage
- **Session Management**: Flask-Login for secure session handling
- **Role-Based Access**: Different permission levels for users and admins
- **Input Validation**: Server-side validation for all endpoints
- **Authentication Required**: Protected endpoints require valid login

## Dependencies

- **Flask 2.3.0**: Web framework
- **Flask-SQLAlchemy 3.1.1**: Database ORM
- **Flask-Login 0.6.2**: User session management
- **PyMySQL 1.1.0**: MySQL database connector
- **BCrypt 4.1.2**: Password hashing
- **Cryptography 41.0.7**: Security operations
