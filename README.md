# Multitenant Todo Task

A Dockerized multi-user todo application using Flask, MySQL, Nginx, Docker Compose, a background worker, and Jenkins CI/CD.

## Team

- Tyron James Beza - Project Lead and Integration
- Rhea Mae Mendoza - Frontend and Quality Assurance
- Kristine Camille Bowman - Backend and Database
- Samantha Maxene Garcia - Infrastructure, Worker, and Jenkins

## Features

- User registration and login
- Private todo lists for each user
- Create, update, complete, and delete todos
- Clear completed todos and per-user statistics
- MySQL data persistence and background activity worker
- Automated Docker tests and Jenkins CI/CD
- Nginx reverse proxy and visible build label

## Technology Stack

- Python 3.12, Flask, and Gunicorn
- MySQL 8.4
- Nginx
- Docker and Docker Compose
- Jenkins
- GitHub

## Project Structure

```text
multitenant-todo-task/
|-- Jenkinsfile                         # pipeline as code
|-- docker-compose.yml                  # application stack
|-- docker-compose.ui-test.yml          # Selenium test services
|-- .env.example                        # safe placeholder values only
|-- .gitignore                          # ignores .env and local files
|-- README.md                           # setup, architecture, team and usage
|-- docs/
|   |-- contribution-log.md             # member contribution record
|   `-- project-proposal.md             # project proposal and roles
|-- proxy/                              # web server and reverse proxy
|   |-- Dockerfile
|   |-- .dockerignore
|   `-- nginx.conf
|-- frontend/                           # browser user interface
|   |-- Dockerfile
|   |-- .dockerignore
|   |-- dockerignore
|   `-- index.html
|-- api/                                # Flask backend service
|   |-- Dockerfile
|   |-- .dockerignore
|   |-- requirements.txt
|   |-- app.py
|   `-- tests/
|       `-- test_app.py
|-- worker/                             # background worker service
|   |-- Dockerfile
|   |-- .dockerignore
|   |-- requirements.txt
|   |-- worker.py
|   `-- tests/
|       `-- test_worker.py
|-- ui-tests/                           # Selenium browser test
|   |-- Dockerfile
|   |-- .dockerignore
|   |-- requirements.txt
|   `-- test_ui.py
|-- db/                                 # MySQL schema and seed setup
|   |-- Dockerfile
|   |-- .dockerignore
|   `-- init.sql
`-- infra/
    `-- jenkins/                        # Jenkins is deployed separately
        |-- Dockerfile
        `-- docker-compose.yml
```

## Requirements

Install only Docker Desktop and Git. Project dependencies are installed inside Docker images; Python, Node.js, MySQL, and Jenkins do not need to be installed directly on the host computer.

## Environment Setup

Copy the safe template:

```powershell
Copy-Item .env.example .env
```

If needed, create `.env` with local values:

```env
MYSQL_ROOT_PASSWORD=choose_a_root_password
DB_HOST=db
DB_NAME=todo_app
DB_USER=todo_user
DB_PASSWORD=choose_a_database_password
TOKEN_SECRET=choose_a_long_secret
TAG=dev
HTTP_PORT=8080
```

Never commit `.env` to GitHub.

## Start and Stop

Start the application:

```powershell
docker compose --env-file .env up -d --build
docker compose --env-file .env ps
```

Open `http://localhost:8080`.

Stop containers without deleting database data:

```powershell
docker compose down
```

Do not use `docker compose down -v` unless you intentionally want to delete the database volume and its records.

## Services and Ports

| Service | Responsibility | Internal port |
| --- | --- | ---: |
| proxy | Nginx reverse proxy and public entry point | 80 |
| frontend | Static web interface | 80 |
| api | Flask API and authentication | 5000 |
| db | MySQL database | 3306 |
| worker | Background activity processing | None |

Only the proxy publishes a host application port: `8080`. All services use the internal Docker network `todo-net`. MySQL stores data in the named volume `todo-db-data`.

## Run Tests

```powershell
docker build --target test -t multitenant-todo-task/api:test ./api
docker build --target test -t multitenant-todo-task/worker:test ./worker
docker compose -f docker-compose.yml -f docker-compose.ui-test.yml --env-file .env up -d selenium
docker compose -f docker-compose.yml -f docker-compose.ui-test.yml --env-file .env run --rm ui-tests
```

A failed unit or Selenium UI test returns a non-zero exit code and blocks the Jenkins pipeline.

## Jenkins

Jenkins runs at `http://localhost:8081`. The pipeline is defined in `Jenkinsfile` and uses:

```text
Repository: https://github.com/ty2k04/multitenant-todo-task.git
Branch: */main
Script Path: Jenkinsfile
```

Pipeline stages:

1. Checkout - downloads the GitHub revision.
2. Test - runs API and worker unit tests.
3. Build Images - builds Docker images.
4. Deploy - starts the Compose application.
5. Smoke Test - checks the frontend and API health endpoint.
6. Selenium UI Test - opens the deployed application in a headless Chrome browser, registers a user, adds a todo, and verifies that it appears.

The Jenkins Secret file credential ID is `multitenant-todo-task-env`. The Jenkinsfile uses the GitHub push trigger. In Jenkins, the job must have **GitHub hook trigger for GITScm polling** enabled under **Build Triggers**. In GitHub, add a repository webhook pointing to `http://<reachable-jenkins-host>/github-webhook/`, select **application/json**, and enable the **Pushes** event. Push a commit and verify that Jenkins starts without clicking **Build Now**.

## Build Tags and Rollback

Jenkins uses the build number as the Docker image tag, for example `multitenant-todo-task/api:3`. The frontend displays the build tag.

List available images:

```powershell
docker images --format "{{.Repository}}:{{.Tag}}" | Select-String "multitenant-todo-task"
```

To use a known-good tag, set it in `.env`:

```env
TAG=2
```

Then start without rebuilding:

```powershell
docker compose --env-file .env up -d --no-build
docker compose ps
```

Rollback preserves MySQL records because the named volume is not removed.

## Data Persistence Test

1. Open `http://localhost:8080` and create a todo.
2. Stop the containers with `docker compose down`.
3. Start them again with `docker compose --env-file .env up -d`.
4. Log in and confirm the todo still exists.

Do not use `down -v` during this test.

## Useful Commands

```powershell
docker compose --env-file .env ps
docker compose images
git log --oneline --decorate --graph --all
docker volume ls
docker compose logs --tail=100 api
docker compose logs --tail=100 db
docker compose logs --tail=100 proxy
```

## Troubleshooting

### Port 8080 is already allocated

Stop the old Compose project using that port, then start this project again:

```powershell
docker compose down
docker compose --env-file .env up -d
```

### API is unhealthy

Check `docker compose logs --tail=100 api` and `docker compose logs --tail=100 db`. Inside Docker, `DB_HOST` must be `db`, not `localhost`, and `DB_PASSWORD` must match the MySQL user password.

### Proxy is restarting

Recreate the network and containers:

```powershell
docker compose down
docker compose --env-file .env up -d --build --force-recreate
```

### Jenkins cannot access GitHub

Use the plain URL `https://github.com/ty2k04/multitenant-todo-task.git`. If the repository is private, configure a GitHub Personal Access Token in Jenkins credentials.
