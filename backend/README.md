# KanMind Backend

KanMind is a REST API backend for a Kanban-style task management application. It was developed with Django and Django REST Framework as part of the Developer Akademie backend curriculum.

The API provides authentication, board management, task management, user assignments, reviews, and comments.

## Features

* User registration and login
* Token-based authentication
* Email-based user accounts
* Create and manage Kanban boards
* Add users as board members
* Create, update, and delete tasks
* Assign tasks to users
* Assign reviewers to tasks
* Filter tasks assigned to the current user
* Filter tasks that the current user has to review
* Create and delete task comments
* Permission-based access control
* Django Admin integration

## Tech Stack

* Python
* Django
* Django REST Framework
* Token Authentication
* SQLite

## Project Structure

```text
backend/
├── auth_app/
│   ├── api/
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   └── models.py
│
├── board/
│   ├── api/
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   └── models.py
│
├── tasks/
│   ├── api/
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   └── models.py
│
├── KanMind/
│   ├── settings.py
│   └── urls.py
│
├── manage.py
└── requirements.txt
```

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>/backend
```

### 2. Create a virtual environment

On Windows:

```bash
python -m venv env
env\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

Optional, but recommended for accessing the Django Admin interface:

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

The API is then available at:

```text
http://127.0.0.1:8000/
```

## Authentication

KanMind uses token-based authentication.

After a successful login, the API returns an authentication token. Protected endpoints require the token in the request header:

```text
Authorization: Token <your-token>
```

The custom user model uses the email address instead of a username for authentication.

## API Overview

### Authentication

The authentication API provides endpoints for:

* User registration
* User login
* User lookup by email

### Boards

Boards contain an owner, members, and tasks.

Available board operations include:

```text
GET     /api/boards/
POST    /api/boards/
GET     /api/boards/{board_id}/
PATCH   /api/boards/{board_id}/
DELETE  /api/boards/{board_id}/
```

Users can only access boards they own or belong to.

Only the board owner is allowed to delete a board.

### Tasks

Tasks belong to a board and can contain an assignee and a reviewer.

Available task operations include:

```text
POST    /api/tasks/
PATCH   /api/tasks/{task_id}/
DELETE  /api/tasks/{task_id}/
```

Additional task endpoints:

```text
GET     /api/tasks/assigned-to-me/
GET     /api/tasks/reviewing/
```

An assignee or reviewer must belong to the corresponding board.

A task can only be deleted by its creator or the owner of the board.

### Comments

Comments belong to tasks.

Available comment operations include:

```text
GET     /api/tasks/{task_id}/comments/
POST    /api/tasks/{task_id}/comments/
DELETE  /api/tasks/{task_id}/comments/{comment_id}/
```

Only board members can access and create comments for tasks on the board.

A comment can only be deleted by its author.

## Permissions

The API uses custom Django REST Framework permissions to protect resources.

Access rules include:

* Authentication is required for protected endpoints.
* Users can only access boards they own or belong to.
* Only board owners can delete boards.
* Only board members can create and update tasks.
* Only task creators or board owners can delete tasks.
* Only board members can access and create comments.
* Only comment authors can delete their comments.

## Data Models

### User

The custom user model uses an email address for authentication and contains:

* Email
* Full name
* Password

### Board

A board contains:

* Title
* Owner
* Members
* Tasks

### Task

A task contains:

* Title
* Description
* Status
* Priority
* Assignee
* Reviewer
* Due date
* Creator
* Board

Supported task statuses:

```text
to-do
in-progress
review
done
```

Supported priorities:

```text
low
medium
high
```

### Comment

A comment contains:

* Author
* Content
* Creation date
* Task

## Database

The project uses SQLite for local development.

The database file is intentionally excluded from version control. After cloning the repository, run:

```bash
python manage.py migrate
```

to create the local database structure.

## Admin Interface

Django Admin can be used to manage application data during development.

After creating a superuser, the admin interface is available at:

```text
http://127.0.0.1:8000/admin/
```

## Development Notes

When sending requests to the API, make sure to include the trailing slash.

Correct:

```text
/api/tasks/
/api/boards/1/
```

Incorrect:

```text
/api/tasks
/api/boards/1
```

This is especially important for `POST`, `PATCH`, and `DELETE` requests because Django cannot always redirect these requests while preserving their request body.

## Requirements

All required Python packages are listed in:

```text
requirements.txt
```

The file can be generated or updated with:

```bash
pip freeze > requirements.txt
```

## Author

Developed as part of the Developer Akademie Python/Django REST Framework curriculum.
