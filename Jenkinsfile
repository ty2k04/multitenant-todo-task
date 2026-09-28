pipeline {
  agent any
  environment { COMPOSE_PROJECT_NAME = 'multitenant-todo-task'; TAG = "${env.BUILD_NUMBER}" }
  triggers { githubPush() }
  options { disableConcurrentBuilds(); buildDiscarder(logRotator(numToKeepStr: '15')) }
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Test') { steps { sh 'docker build --target test -t multitenant-todo-task/api:test ./api'; sh 'docker build --target test -t multitenant-todo-task/worker:test ./worker' } }
    stage('Build Images') { steps { sh 'docker compose build' } }
    stage('Deploy') {
      steps {
        withCredentials([file(credentialsId: 'multitenant-todo-task-env', variable: 'ENV_FILE')]) {
          sh 'cp "$ENV_FILE" .env && docker compose up -d --no-build --remove-orphans'
        }
      }
    }
    stage('Smoke Test') {
      steps {
        sh '''
          for i in $(seq 1 18); do
            if docker compose exec -T proxy wget -qO- http://frontend/ >/dev/null 2>&1 && docker compose exec -T api python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"; then echo "Smoke test passed"; exit 0; fi
            sleep 5
          done
          echo "Smoke test failed"; exit 1
        '''
      }
    }
  }
  post {
    success { echo "Build ${TAG} is live" }
    failure { echo "Build ${TAG} failed" }
    always { sh 'rm -f .env' }
  }
}

