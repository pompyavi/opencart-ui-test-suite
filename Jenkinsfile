pipeline {
  agent { label 'windows' } // uses a Windows node (required for bat + Docker Desktop)

  options {
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '20'))
    timeout(time: 60, unit: 'MINUTES')
  }

  triggers {
    // Build on GitHub push (make sure your repo webhook points to /github-webhook/)
    githubPush()
  }

  parameters {
    choice(name: 'TEST_ENV', choices: ['qa', 'uat', 'prod'], description: 'Target test environment')
    choice(name: 'browser', choices: ['chrome', 'firefox'], description: 'Target browser')
    string(name: 'browser_version', defaultValue: 'latest', description: 'Browser version (e.g. latest, 126, etc.)')
    booleanParam(name: 'REMOTE', defaultValue: true, description: 'Run via Selenoid (Docker). If false, run local.')
    string(name: 'MARK', defaultValue: '', description: 'Optional pytest -m filter (e.g. "smoke and not flaky")')
  }

  environment {
    // Your tests read env = os.getenv("TEST_ENV", "qa")
    TEST_ENV = "${params.TEST_ENV}"

    REPORTS_DIR = 'reports'
    ALLURE_DIR  = 'reports\\allure-results'
    SELENOID_COMPOSE = 'selenoid\\docker-compose.yml'

    REPO_URL    = 'https://github.com/pompyavi/opencart-ui-test-suite.git'
    REPO_BRANCH = 'main'
  }

  stages {
    stage('Checkout (clean)') {
      steps {
        deleteDir()
        checkout([
          $class: 'GitSCM',
          branches: [[name: "*/${REPO_BRANCH}"]],
          userRemoteConfigs: [[url: "${REPO_URL}"]],
          extensions: [[ $class: 'CleanBeforeCheckout' ]]
        ])
      }
    }

    stage('Python venv + deps') {
      steps {
        bat '''
          if not exist ".venv\\Scripts\\python.exe" (
            py -3 -m venv .venv || python -m venv .venv
          )
          call .\\.venv\\Scripts\\activate.bat
          python -m pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Prep report folders') {
      steps {
        bat '''
          if exist "%REPORTS_DIR%" rmdir /s /q "%REPORTS_DIR%"
          mkdir "%REPORTS_DIR%"
          mkdir "%ALLURE_DIR%"
        '''
      }
    }

    stage('Start Selenoid (if REMOTE)') {
      when { expression { return params.REMOTE == true } }
      steps {
        bat '''
          REM Start Docker Desktop (headless) and wait until engine is ready
          docker desktop start

          for /l %%i in (1,1,60) do (
            docker info >nul 2>&1 && goto _docker_ready
            timeout /t 2 >nul
          )
          echo Docker didn't start in time. & exit /b 1
          :_docker_ready

          docker compose -f "%SELENOID_COMPOSE%" up -d
        '''
      }
    }

    stage('Run tests') {
      steps {
    bat """
      call .\\.venv\\Scripts\\activate.bat && ^
      python -m pytest --browser ${params.browser} --browser_version ${params.browser_version} ${params.REMOTE ? '--remote' : ''} -n auto --dist loadscope --alluredir=%ALLURE_DIR% --junitxml=%REPORTS_DIR%\\junit.xml --html=%REPORTS_DIR%\\latest.html --self-contained-html
    """
    }
    }
  }

  post {
    always {
      script {
        if (params.REMOTE == true) {
          bat 'docker compose -f "%SELENOID_COMPOSE%" down || ver >nul'
        }
      }

      // JUnit (for test trend)
      junit allowEmptyResults: false,
            keepProperties: true,
            keepTestNames: true,
            testResults: 'reports/junit.xml'

      // Allure (needs Allure Jenkins plugin)
      allure includeProperties: false,
             results: [[path: 'reports/allure-results']]

      // Publish pytest HTML report (latest.html)
      publishHTML(target: [
        reportName: 'Pytest HTML Report',
        reportDir: 'reports',
        reportFiles: 'latest.html',
        alwaysLinkToLastBuild: false,
        keepAll: true,
        allowMissing: false,
        includes: '**/*',
        escapeUnderscores: true,
        useWrapperFileDirectly: true,
        numberOfWorkers: 0
      ])

      // Archive all report artifacts
      archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
    }
  }
}
