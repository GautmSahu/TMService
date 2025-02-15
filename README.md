# TMService
Task Management Restful Services

# Objective
Build a lightweight task management microservice that includes basic task operations, user roles, and a minimal notification system. This project will test skills in microservices, PostgreSQL database design, and API development in Django/Python.

# Project Requirements

1. Task Management Microservice:

    - Create a microservice to manage tasks, with fields for title, description, status (e.g., “To Do,” “In Progress,” “Completed”), and a due date.
    - Implement CRUD operations for tasks.
    - Allow tasks to be assigned to a user, with the ability to reassign as needed.

2. User Management Microservice:

    - Set up a basic user management service with two roles: admin and regular user.
    - Admins can create and manage tasks, while regular users can only view tasks assigned to them.
    - Include JWT-based authentication and authorization for securing endpoints.

3. Notification System:

    - Implement a minimal notification service that sends an alert when a task's status is updated or a task is close to its due date.
    - Use Django Signals for event handling within the Task Management microservice to trigger notifications.
    - Deliver notifications via email or as log entries (as a lightweight alternative to a separate notification microservice).

4. Database Design:

    - Use PostgreSQL to store data for both tasks and users.
    - Structure the database to support relationships between users and tasks, with appropriate indexing for efficient querying.

5. API Requirements:

    - Develop RESTful APIs for both microservices, following best practices.
    - Enable filtering for tasks by status or due date.
    - Provide endpoint documentation for ease of testing and integration.
6. Documentation:

    - Provide a README with setup instructions, an overview of the architecture, and brief explanations of the main components.
    - Include sample API requests for each endpoint.
    - Deployment: Deploy the project to a live environment and provide a URL along with the GitHub repository. You can use any free hosting service (e.g., Heroku, Render, Railway) or a personal VPS if available.
    - Environment Setup: Include any necessary environment variables or setup instructions in a .env.example file (without sensitive data) for easy configuration.


# Task Management Microservice Architecture

1. Overview
The Task Management Microservice is a modular system designed to handle task operations, user roles, authentication, and notifications efficiently. The architecture follows microservices principles, with a clear separation of concerns between task management, user authentication, and notifications.

2. Architecture Diagram

    -       +----------------------+      +----------------------+      +----------------------+
            |   Task Microservice  | <--> |   User Microservice  | <--> | Notification Service |
            |  (Django + DRF)      |      |  (Django + DRF)      |      |  (Django Signals)    |
            +----------------------+      +----------------------+      +----------------------+
                    |                           |                          |
                    |                           |                          |
                    v                           v                          v
            +-----------------+           +-----------------+         +------------------------+
            |  PostgreSQL DB  |           |  PostgreSQL DB  |         |  Logging System (File) |
            |  (Tasks Table)  |           |  (Users Table)  |         |  & Cron Jobs for Alerts|
            +-----------------+           +-----------------+         +------------------------+
                    |
                    v
            +----------------------+
            |   API Gateway (Nginx)|
            |  - Reverse Proxy     |
            |  - Load Balancing    |
            +----------------------+
                    |
                    v
            +------------------------+
            |   Clients (Web/Mobile) |
            |  - React, Vue, etc.    |
            +------------------------+


3. Components & Their Roles
    - Task Management Microservice
        - Handles:
        - CRUD operations for tasks (Create, Read, Update, Delete).
        - Assigning tasks to users.
        - Filtering tasks by status and due date.
        - Endpoints:
            - POST /task/tasks/ → Create a new task
            - GET /task/tasks/ → List all tasks
            - GET /task/tasks/{id}/ → Retrieve a single task
            - PUT /task/tasks/{id}/ → Update a task
            - DELETE /task/tasks/{id}/ → Delete a task
            - GET /task/tasks?status=completed → Filter tasks
        - Database:
            - Task (id, title, description, status, due_date, assigned_to)
        - Security & Authorization:
            - Admins can create, update, and delete tasks.
            - Regular users can only view their assigned tasks.
            - Uses JWT authentication for security.

    - User Management Microservice
        - Handles:
            - User registration and authentication.
            - Role-based access control (Admin/User).
        - JWT-based authentication.
        - Endpoints:
            - POST /user/register/ → Register a new user
            - POST /token/ → Obtain JWT token
            - POST /token/refresh/ → Refresh token
            - GET /user/users/ → Get all users
            - PUT /user/users/ → Update user
            - DELETE /user/users/ → Delete user
        - Database:
            - User (id, username, email, password, role)
        - Security & Authorization:
            - Uses django.contrib.auth for authentication.
        - Role validation: Only Admins can manage users and tasks.
    
    - Notification Service
        - Handles:
            - Sending alerts when task status changes or is close to the due date.
            - Logging notifications (instead of a separate database).
        - Implementation:
            - Uses Django Signals to trigger notifications.
            - Uses CronJobs for due date reminders.
            - Logs notifications instead of using a separate model.

4. Technologies Used
    - Backend: Django, Django REST Framework (DRF)
    - Database: PostgreSQL
    - Authentication: JWT (Django Simple JWT)
    - Logging & Monitoring: Python Logging, CronJobs
    - Throttling: DRF's ScopedRateThrottle
        - Throttling Implementation
            - Used Django REST Framework's ScopedRateThrottle, allowing us to define different rate limits for admins and users.
                - Admin/Regular Users: 10 requests per minute
                - Anonymous user: 5 requests per minute

5. Deployment Strategy
    - Nginx + Gunicorn for serving Django.
    - render.com for free hosting

6. Live Links
    - [Website URL](https://tmservice.onrender.com/)
    - [Github Repo](https://github.com/GautmSahu/TMService)
    - [Postman Collection and API Documentation](https://drive.google.com/file/d/1fXTx3e6_p3qnoqSauvH8TkOWzgaEGf-C/view?usp=sharing)

# Note
    - Used free domain server from render.com for hosting, so for 1st time the api/web may respond late and may take upto 1 minute.
    - As its a third party and free server, i have not setup the cronjob for task notification but it will run perfectly on local system.

# Steps for setting up on local system (ubuntu)
    - Clone git repo
        - git clone https://github.com/GautmSahu/TMService.git
    - Create virtual environment(python=3.11)
        - python3 -m venv venv
    - Activate the environment
        - . venv/bin/activate
    - Go to project path
        - cd TMService/
    - Install required packages
        - pip install -r requirements.txt
    - Open .env file and do the necessary changes like DB configuration etc.
    - Export the environment variables
        - source .env
    - Run migrations
        - python manage.py makemigrations
        - python manage.py migrate
    - Seup cronjob for task notification
        - crontab -e
            - 0 8 * * * /path/to/your/venv/bin/python /path/to/your/project/manage.py check_due_tasks
            - save and exit
    - Run the django server
        - python manage.py runserver
    - That's it.

