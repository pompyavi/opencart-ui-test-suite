pipeline {
  agent any

  options {
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '20'))
    timeout(time: 60, unit: 'MINUTES')
  }

  triggers {
    githubPush()
  }

  parameters {
    choice(name: 'ENV', choices: ['qa','uat','prod'], description: 'Target Environment')
    choice(name: 'browser', choices: ['chrome','firefox'], description: 'Browser')
    string(name: 'browser_version', defaultValue: 'latest', description: 'Browser Version')
    booleanParam(name: 'remote', defaultValue: false, description: 'Run via Docker Grid (Selenoid)')
    booleanParam(name: 'saucelabs', defaultValue: false, description: 'Run via SauceLabs')
  }

  environment {
    REPORTS_DIR = 'reports'
    ALLURE_DIR  = 'reports/allure-results'
    SELENOID_COMPOSE = 'selenoid/docker-compose.yml'
  }

  stages {

    stage('Checkout') {
      steps {
        deleteDir()
        checkout scm
      }
    }

    stage('Create Virtual Environment') {
      steps {
        sh '''
        if [ ! -d ".venv" ]; then
          python3 -m venv .venv
        fi
        '''
      }
    }

    stage('Install Dependencies') {
      steps {
        sh '''
        source .venv/bin/activate
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        '''
      }
    }

    stage('Prepare Reports') {
      steps {
        sh '''
        rm -rf "$REPORTS_DIR"
        mkdir -p "$ALLURE_DIR"
        '''
      }
    }

    stage('Start Docker Grid (if remote)') {
      when { expression { params.remote == true && params.saucelabs == false } }
      steps {
        sh '''
        echo "Starting Docker…"
        open -a Docker || true

        # wait for docker to be ready
        for i in {1..60}; do
          docker info >/dev/null 2>&1 && break
          sleep 2
        done || { echo "Docker not ready"; exit 1; }

        docker compose -f "$SELENOID_COMPOSE" up -d
        '''
      }
    }

    stage('Run Tests') {
      steps {
        sh '''
        source .venv/bin/activate

        # safety: remote and saucelabs cannot both be true
        if [ "${remote}" = "true" ] && [ "${saucelabs}" = "true" ]; then
          echo "ERROR: remote and saucelabs cannot both be true"
          exit 1
        fi

        CMD="python -m pytest \
          --env ${ENV} \
          --browser ${browser} \
          --browser_version ${browser_version} \
          -n auto --dist loadscope \
          --alluredir=${ALLURE_DIR} \
          --junitxml=${REPORTS_DIR}/junit.xml \
          --html=${REPORTS_DIR}/report.html --self-contained-html"

        if [ "${saucelabs}" = "true" ]; then
          echo "Running on SauceLabs"
          CMD="$CMD --saucelabs"
        elif [ "${remote}" = "true" ]; then
          echo "Running on Docker Grid"
          CMD="$CMD --remote"
        else
          echo "Running Locally"
        fi

        echo "$CMD"
        set +e
        eval "$CMD"
        status=$?
        set -e
        exit $status
        '''
      }
    }
  }

  post {
    always {

      script {
        if (params.remote == true && params.saucelabs == false) {
          sh 'docker compose -f "$SELENOID_COMPOSE" down || true'
        }
      }

      // JUnit report
      junit 'reports/junit.xml'

      // Allure report
      allure([
        includeProperties: false,
        results: [[path: 'reports/allure-results']]
      ])

      // Pytest HTML
      publishHTML(target: [
        reportName: 'Pytest HTML Report',
        reportDir: 'reports',
        reportFiles: 'report.html',
        alwaysLinkToLastBuild: true,
        keepAll: true,
        allowMissing: false
      ])

      archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
    }

    success {
      echo "BUILD SUCCESS"
    }

    failure {
      echo "BUILD FAILED"
    }
  }
}
