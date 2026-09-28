# From Scratch Group Build Guide

This guide explains how the four members will build the Multitenant Todo Task App from an initially empty GitHub repository. It is designed so each member creates source code for their own role and GitHub records the work through branches, commits, and pull requests.

The existing complete project is a backup only. Do not copy its finished source files into the new group repository if the purpose is to demonstrate contributions from the beginning.

## Team members and responsibilities

### Tyron James Beza

Role: Project Lead, Scrum Master, Integration, and final verification.

Tyron creates the empty repository, team plan, folder structure, project proposal, final documentation, and presentation. Tyron reviews and merges pull requests and performs final integration.

Tyron should not upload the finished application before the other members contribute.

### Rhea Mae Mendoza

Role: Frontend and Quality Assurance.

Rhea creates the user interface, frontend Dockerfile, task interactions, task counter, clear-completed feature, and frontend testing notes.

### Kristine Camille Bowman

Role: Backend and Database.

Kristine creates the Flask API, MySQL schema, authentication behavior, todo endpoints, API tests, and per-user data protection.

### Samantha Maxene Garcia

Role: Infrastructure, Worker, and Jenkins.

Samantha creates the background worker, Dockerfiles, Docker Compose configuration, Nginx proxy, Jenkins Docker setup, Jenkinsfile, and infrastructure verification.

## Part 1 Tyron creates the empty GitHub repository

1. Sign in to GitHub.
2. Click the plus sign in the upper-right corner.
3. Click New repository.
4. Name the repository:

~~~text
multitenant-todo-task
~~~

5. Select Private unless the instructor requires Public.
6. Do not add a README.
7. Do not add a .gitignore.
8. Do not add a license.
9. Click Create repository.

## Part 2 Tyron creates the first local commit

Create a new local folder. Do not use the completed project folder as the new repository.

~~~powershell
New-Item -ItemType Directory -Path "D:\multitenant-todo-task"
cd "D:\multitenant-todo-task"
git init -b main
git config user.name "Tyron James Beza"
git config user.email "TYRON_VERIFIED_GITHUB_EMAIL"
~~~

Create only these initial files:

~~~text
README.md
.gitignore
docs/project-proposal.md
docs/contribution-log.md
~~~

Create only the empty folders:

~~~text
api/
db/
frontend/
worker/
proxy/
infra/jenkins/
docs/
~~~

The first commit should contain planning and structure, not the complete application.

~~~powershell
git add README.md .gitignore docs
git add api db frontend worker proxy infra
git commit -m "Create group project structure and team plan"
git remote add origin https://github.com/TYRON_GITHUB_USERNAME/multitenant-todo-task.git
git push -u origin main
~~~

Replace the uppercase placeholders with Tyron's actual GitHub username and verified email.

## Part 3 Tyron invites the members

On the repository page:

1. Click Settings.
2. Click Collaborators.
3. Click Add people.
4. Invite Rhea Mae Mendoza.
5. Invite Kristine Camille Bowman.
6. Invite Samantha Maxene Garcia.
7. Wait for all invitations to be accepted.

Create and assign these Issues:

~~~text
Issue 1: Build frontend and QA tests - Rhea Mae Mendoza
Issue 2: Build Flask API and MySQL database - Kristine Camille Bowman
Issue 3: Build Docker infrastructure worker and Jenkins - Samantha Maxene Garcia
Issue 4: Final integration documentation and presentation - Tyron James Beza
~~~

## Part 4 Common setup for every member

Each member must use their own GitHub account and verified email.

~~~powershell
git clone https://github.com/TYRON_GITHUB_USERNAME/multitenant-todo-task.git
cd multitenant-todo-task
git config user.name "YOUR REAL NAME"
git config user.email "YOUR VERIFIED GITHUB EMAIL"
git checkout main
git pull origin main
~~~

Each member creates a separate branch. Nobody works directly on main.

## Part 5 Rhea creates the frontend source code

Rhea creates the branch:

~~~powershell
git checkout main
git pull origin main
git checkout -b rhea-frontend
~~~

Rhea creates:

~~~text
frontend/index.html
frontend/Dockerfile
frontend/.dockerignore
~~~

The frontend must include:

- Username field
- Password field
- Register button
- Login button
- Todo input
- Add button
- Todo list
- Checkbox for completing tasks
- Delete button
- Logout button
- Active-task counter
- Clear completed button
- Activity notification list

The frontend must call these API paths:

~~~text
POST /api/auth/register
POST /api/auth/login
GET /api/todos
POST /api/todos
PATCH /api/todos/:id
DELETE /api/todos/:id
GET /api/notifications
~~~

The frontend Dockerfile should serve the page with Nginx.

Example frontend Dockerfile:

~~~dockerfile
FROM nginx:1.27-alpine
COPY index.html /usr/share/nginx/html/index.html
ARG BUILD_TAG=dev
RUN sed -i "s/__BUILD_TAG__/\${BUILD_TAG}/g" /usr/share/nginx/html/index.html
~~~

Rhea tests the HTML file after Samantha provides the proxy and Compose configuration. Rhea should commit the user interface first and later make a follow-up commit for any integration fixes.

~~~powershell
git add frontend
git commit -m "Build todo frontend and authentication interface"
git push -u origin rhea-frontend
~~~

Rhea opens a pull request into main titled:

~~~text
Build todo frontend and authentication interface
~~~

Rhea includes screenshots and explains the files created.

After the API exists, Rhea adds the task counter and clear-completed behavior in a second commit:

~~~powershell
git add frontend/index.html
git commit -m "Add task counter and clear completed feature"
git push
~~~

## Part 6 Kristine creates the backend and database source code

Kristine creates the branch:

~~~powershell
git checkout main
git pull origin main
git checkout -b kristine-api-database
~~~

Kristine creates:

~~~text
api/app.py
api/Dockerfile
api/requirements.txt
api/tests/test_app.py
api/.dockerignore
db/Dockerfile
db/init.sql
db/.dockerignore
~~~

The database schema must create these tables:

~~~text
users
todos
notifications
~~~

The users table stores usernames and password hashes.

The todos table stores:

~~~text
id
user_id
title
completed
notified
created_at
~~~

The notifications table stores:

~~~text
id
user_id
message
created_at
~~~

The API must implement:

~~~text
GET /health
POST /api/auth/register
POST /api/auth/login
GET /api/todos
POST /api/todos
PATCH /api/todos/:id
DELETE /api/todos/:id
GET /api/notifications
GET /api/stats
~~~

The API must:

- Validate registration input.
- Hash passwords with SHA-256 in MySQL.
- Return a token after registration and login.
- Require authentication for private routes.
- Filter every todo query by the authenticated user ID.
- Prevent one user from reading or changing another user's tasks.
- Return total, completed, and pending counts from /api/stats.

Kristine's API requirements file should include Flask, Gunicorn, and mysql-connector-python. The Dockerfile must include a test stage.

The API tests must cover:

~~~text
Public health route
Token creation and validation
Tampered token rejection
Unauthenticated todo requests
Unauthenticated statistics requests
Statistics route registration
~~~

Kristine runs:

~~~powershell
docker build --target test -t multitenant-todo-task/api:test ./api
~~~

Kristine commits and pushes:

~~~powershell
git add api db
git commit -m "Build Flask API MySQL schema and API tests"
git push -u origin kristine-api-database
~~~

Kristine opens a pull request into main titled:

~~~text
Build Flask API MySQL schema and API tests
~~~

## Part 7 Samantha creates infrastructure and Jenkins source code

Samantha creates the branch:

~~~powershell
git checkout main
git pull origin main
git checkout -b samantha-docker-jenkins
~~~

Samantha creates:

~~~text
worker/worker.py
worker/Dockerfile
worker/requirements.txt
worker/tests/test_worker.py
worker/.dockerignore
proxy/Dockerfile
proxy/nginx.conf
proxy/.dockerignore
docker-compose.yml
Jenkinsfile
infra/jenkins/Dockerfile
infra/jenkins/docker-compose.yml
~~~

The worker must:

- Connect to MySQL.
- Find todos that have not been notified.
- Create notifications.
- Mark processed todos as notified.
- Continue retrying if the database is temporarily unavailable.

The worker Dockerfile must include a test stage.

Samantha adds a worker health-check script that connects to MySQL and exits with code 0 when successful and code 1 when unsuccessful.

The Compose file must define:

~~~text
proxy
frontend
api
worker
db
~~~

It must include:

- A named MySQL volume.
- A shared Docker network.
- MySQL health checks.
- API dependency on healthy MySQL.
- Worker dependency on healthy MySQL.
- API health checks.
- Port 8080 for the application.
- Environment variables from .env.example.

The Jenkinsfile must include stages for:

~~~text
Checkout
Test
Build Images
Deploy
Smoke Test
~~~

Jenkins must run inside Docker. Samantha must not require Jenkins to be installed directly on the host.

Samantha validates:

~~~powershell
docker compose --env-file .env.example config
docker build --target test -t multitenant-todo-task/worker:test ./worker
docker compose --env-file .env.example up -d --build
docker compose --env-file .env.example ps
~~~

Samantha commits and pushes:

~~~powershell
git add worker proxy docker-compose.yml Jenkinsfile infra
git commit -m "Build Docker infrastructure worker and Jenkins pipeline"
git push -u origin samantha-docker-jenkins
~~~

Samantha opens a pull request into main titled:

~~~text
Build Docker infrastructure worker and Jenkins pipeline
~~~

## Part 8 Tyron integrates the team work

Tyron reviews the three pull requests.

For each pull request, verify:

- The author is the correct member.
- The branch is correct.
- The changed files match the assigned role.
- The commit message describes real work.
- The member included test evidence.
- No unrelated files were copied from the old completed project.
- The pull request description is accurate.

Merge the pull requests in this order:

1. Kristine's API and database pull request.
2. Rhea's frontend pull request.
3. Samantha's infrastructure pull request.

If the frontend or infrastructure work needs an update after another pull request is merged, the member creates another commit on the same branch and updates the pull request.

## Part 9 Final integration commands

After all pull requests are merged:

~~~powershell
cd "D:\multitenant-todo-task"
git checkout main
git pull origin main
docker build --target test -t multitenant-todo-task/api:test ./api
docker build --target test -t multitenant-todo-task/worker:test ./worker
docker compose --env-file .env.example config
docker compose --env-file .env.example up -d --build
docker compose --env-file .env.example ps
~~~

Test the application at:

~~~text
http://localhost:8080
~~~

Test two separate users. Each user must see only their own tasks.

Start Jenkins:

~~~powershell
docker compose -f infra/jenkins/docker-compose.yml up -d --build
~~~

Open:

~~~text
http://localhost:8081
~~~

Configure Jenkins as Pipeline from SCM using the repository URL and the root Jenkinsfile.

## Part 10 Final documentation

Tyron completes:

~~~text
docs/technical-documentation.md
docs/presentation-script.md
docs/architecture.svg
docs/contribution-log.md
README.md
~~~

The contribution log must contain actual names, usernames, branch names, commit URLs, pull-request URLs, merge dates, and screenshots or other evidence.

Do not enter invented commit links, pull-request links, dates, or screenshots. The purpose of this guide is to make the work real and individually traceable.

## Final evidence checklist

Collect:

- Repository creation date
- Initial team-structure commit
- GitHub collaborator list
- Assigned Issues
- Rhea's frontend branch and commits
- Kristine's backend and database branch and commits
- Samantha's infrastructure branch and commits
- All pull requests
- Merged pull requests
- GitHub contributor graph
- API Docker test output
- Worker Docker test output
- Docker Compose status
- Application screenshots
- Jenkins successful build
- Final documentation and presentation
