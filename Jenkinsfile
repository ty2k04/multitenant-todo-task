pipeline {
  agent any
  environment { COMPOSE_PROJECT_NAME = 'multitenant-todo-task'; TAG = "${env.BUILD_NUMBER}" }
  triggers { githubPush() }
  options { disableConcurrentBuilds(); buildDiscarder(logRotator(numToKeepStr: '15')) }
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Test') {
      steps {
        sh '''
          set -e
          mkdir -p test-results
          docker build --target test -t multitenant-todo-task/api:test ./api
          docker build --target test -t multitenant-todo-task/worker:test ./worker

          docker create --name api-unit-test multitenant-todo-task/api:test pytest -q --junitxml=/tmp/api-junit.xml
          set +e
          docker start -a api-unit-test
          api_status=$?
          set -e
          docker cp api-unit-test:/tmp/api-junit.xml test-results/api-junit.xml || true
          docker rm api-unit-test

          docker create --name worker-unit-test multitenant-todo-task/worker:test pytest -q --junitxml=/tmp/worker-junit.xml
          set +e
          docker start -a worker-unit-test
          worker_status=$?
          set -e
          docker cp worker-unit-test:/tmp/worker-junit.xml test-results/worker-junit.xml || true
          docker rm worker-unit-test

          if [ "$api_status" -ne 0 ] || [ "$worker_status" -ne 0 ]; then
            exit 1
          fi
        '''
      }
      post {
        always {
          junit testResults: 'test-results/*.xml', allowEmptyResults: false
        }
      }
    }
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
    stage('Selenium UI Test') {
      steps {
        withCredentials([file(credentialsId: 'multitenant-todo-task-env', variable: 'ENV_FILE')]) {
          sh '''
            cp "$ENV_FILE" .env
            docker compose -f docker-compose.yml -f docker-compose.ui-test.yml --env-file .env up -d selenium
            docker compose -f docker-compose.yml -f docker-compose.ui-test.yml --env-file .env run --rm ui-tests
          '''
        }
      }
      post {
        always {
          sh 'docker compose -f docker-compose.yml -f docker-compose.ui-test.yml --env-file .env stop selenium || true'
        }
      }
    }
  }
  post {
    success { echo "Build ${TAG} is live" }
    failure { echo "Build ${TAG} failed" }
    always { sh 'rm -f .env' }
  }
}

