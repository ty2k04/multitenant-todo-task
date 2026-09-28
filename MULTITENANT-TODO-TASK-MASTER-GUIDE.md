# Multitenant Todo Task Master Group Guide

## Purpose

This is the master guide for the four-member project. The GitHub repository will be named:

~~~text
multitenant-todo-task
~~~

The project must be built from an initially empty repository so GitHub records each member's real source-code contribution.

The existing completed project is only a backup. Do not copy its finished source code into the new repository before the assigned member creates that source code.

## Members and ownership

| Member | Ownership |
| --- | --- |
| Tyron James Beza | Repository setup, planning, integration, final documentation, presentation, and final verification |
| Rhea Mae Mendoza | Frontend source code and frontend quality assurance |
| Kristine Camille Bowman | Flask API, MySQL schema, authentication, todo endpoints, and API tests |
| Samantha Maxene Garcia | Worker, Dockerfiles, Docker Compose, proxy, Jenkins, and infrastructure verification |

## Required GitHub history

The final repository should show:

1. Tyron's initial planning and folder-structure commit.
2. Rhea's frontend branch and commits.
3. Kristine's API and database branch and commits.
4. Samantha's infrastructure and Jenkins branch and commits.
5. Pull requests from each member.
6. Reviews and merges into main.
7. Final integration commits by Tyron.

Every member must use their own GitHub account and verified email. Do not create fake commits, backdate commits, or upload another member's work using the wrong account.

## Repository creation

Tyron creates an empty GitHub repository named multitenant-todo-task. Do not add GitHub's README, .gitignore, or license.

Tyron then creates a new local folder and initializes Git:

~~~powershell
New-Item -ItemType Directory -Path "D:\multitenant-todo-task"
cd "D:\multitenant-todo-task"
git init -b main
git config user.name "Tyron James Beza"
git config user.email "TYRON_VERIFIED_GITHUB_EMAIL"
~~~

The first commit contains only:

~~~text
README.md
.gitignore
docs/project-proposal.md
docs/contribution-log.md
~~~

and the empty folders:

~~~text
api/
db/
frontend/
worker/
proxy/
infra/jenkins/
docs/
~~~

Tyron commits and pushes:

~~~powershell
git add README.md .gitignore docs MULTITENANT-TODO-TASK-MASTER-GUIDE.md FROM-SCRATCH-GROUP-BUILD-GUIDE.md
git add api db frontend worker proxy infra
git commit -m "Create group project structure and team plan"
git remote add origin https://github.com/TYRON_GITHUB_USERNAME/multitenant-todo-task.git
git push -u origin main
~~~

## Member workflow

Each member:

1. Accepts the GitHub invitation.
2. Clones the repository.
3. Sets their own Git name and verified GitHub email.
4. Creates their assigned branch.
5. Creates only their assigned source files.
6. Runs Docker tests when their part is testable.
7. Commits the work.
8. Pushes the branch.
9. Opens a pull request into main.
10. Sends the pull-request URL to Tyron.

No member works directly on main.

## Rhea's required files

Branch:

~~~text
rhea-frontend
~~~

Files:

~~~text
frontend/index.html
frontend/Dockerfile
frontend/.dockerignore
~~~

The frontend must contain registration, login, todo creation, completion, deletion, logout, active-task counter, clear-completed button, and activity notifications.

Rhea commits:

~~~powershell
git add frontend
git commit -m "Build frontend and authentication interface"
git push -u origin rhea-frontend
~~~

Rhea later adds a follow-up commit for the task counter and clear-completed behavior if the first pull request does not include them.

## Kristine's required files

Branch:

~~~text
kristine-api-database
~~~

Files:

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

The API must implement authentication, todo ownership, todo CRUD, notifications, health, and per-user statistics. The database must contain users, todos, and notifications tables.

Kristine runs:

~~~powershell
docker build --target test -t multitenant-todo-task/api:test ./api
~~~

Kristine commits:

~~~powershell
git add api db
git commit -m "Build Flask API MySQL schema and API tests"
git push -u origin kristine-api-database
~~~

## Samantha's required files

Branch:

~~~text
samantha-docker-jenkins
~~~

Files:

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

Samantha's infrastructure must include the API, frontend, worker, database, and proxy services; a named MySQL volume; a shared network; health checks; Docker test stages; and Jenkins stages for Checkout, Test, Build Images, Deploy, and Smoke Test.

Samantha runs:

~~~powershell
docker compose --env-file .env.example config
docker build --target test -t multitenant-todo-task/worker:test ./worker
docker compose --env-file .env.example up -d --build
docker compose --env-file .env.example ps
~~~

Samantha commits:

~~~powershell
git add worker proxy docker-compose.yml Jenkinsfile infra
git commit -m "Build Docker infrastructure worker and Jenkins pipeline"
git push -u origin samantha-docker-jenkins
~~~

## Tyron's review and merge

Tyron checks each pull request for the correct author, branch, files, tests, and description. Tyron merges:

1. Kristine's API and database pull request.
2. Rhea's frontend pull request.
3. Samantha's infrastructure pull request.

If a member needs to fix something, that member pushes another commit to their own branch.

## Final verification

After the pull requests are merged:

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

Open http://localhost:8080.

Test two users and verify that each user sees only their own todo list.

Start Jenkins:

~~~powershell
docker compose -f infra/jenkins/docker-compose.yml up -d --build
~~~

Open http://localhost:8081, configure Pipeline from SCM using the repository root Jenkinsfile, and run Build Now.

## Evidence to collect

Collect the repository page, collaborators, issues, branches, individual commits, pull requests, merged pull requests, contributor graph, Docker test output, Docker container status, two-user test, Jenkins build, screenshots, final documentation, and presentation.

The contribution log must be updated with actual GitHub usernames, commit URLs, pull-request URLs, merge dates, and evidence only after the work is genuinely completed.

## Fix for the README pathspec error

If Git says `pathspec 'README.md' did not match any files`, README.md has not been created in the current folder yet. Run these commands from the new repository folder:

~~~powershell
cd "D:\multitenant-todo-task"
Get-ChildItem -Force
~~

The new repository must contain README.md, .gitignore, and docs before the first add command. The starter files are already prepared at:

~~~text
D:\multitenant-todo-task\README.md
D:\multitenant-todo-task\.gitignore
D:\multitenant-todo-task\docs\project-proposal.md
D:\multitenant-todo-task\docs\contribution-log.md
~~~

Tyron can now run:

~~~powershell
cd "D:\multitenant-todo-task"
git add README.md .gitignore docs
git commit -m "Create group project structure and team plan"
git push -u origin main
~~~

If the files are missing, copy the starter files from D:\multitenant-todo-task-source-packets\Tyron into the repository first.

## Copy-paste source-code packets

The source packets are stored outside the Git repository so the members can add their own assigned files through their own branches:

~~~text
D:\multitenant-todo-task-source-packets\Tyron
D:\multitenant-todo-task-source-packets\Rhea
D:\multitenant-todo-task-source-packets\Kristine
D:\multitenant-todo-task-source-packets\Samantha
~~~

These packets contain the source files to use as the starting implementation. Each member must understand, test, and commit their own assigned packet from their own GitHub account. The packet itself is not evidence of a completed contribution until the member creates a branch, makes the commit, opens the pull request, and performs the verification.

### Tyron packet

Copy the planning files before the first commit:

~~~powershell
Copy-Item "D:\multitenant-todo-task-source-packets\Tyron\README.md" .\README.md -Force
Copy-Item "D:\multitenant-todo-task-source-packets\Tyron\.gitignore" .\.gitignore -Force
Copy-Item "D:\multitenant-todo-task-source-packets\Tyron\project-proposal.md" .\docs\project-proposal.md -Force
Copy-Item "D:\multitenant-todo-task-source-packets\Tyron\contribution-log.md" .\docs\contribution-log.md -Force
~~~

### Rhea packet

Rhea copies the contents of D:\multitenant-todo-task-source-packets\Rhea\frontend into the repository's frontend folder, reviews the code, tests it, and commits the files on branch rhea-frontend.

### Kristine packet

Kristine copies the api and db folders from D:\multitenant-todo-task-source-packets\Kristine into the repository, reviews the code, runs the API Docker tests, and commits the files on branch kristine-api-database.

### Samantha packet

Samantha copies the worker, proxy, infra, docker-compose.yml, and Jenkinsfile from D:\multitenant-todo-task-source-packets\Samantha into the repository, reviews the code, runs the Docker checks, and commits the files on branch samantha-docker-jenkins.

The source packets are prepared for copying, but each member is still responsible for the review, testing, commit, push, and pull request associated with the work.
