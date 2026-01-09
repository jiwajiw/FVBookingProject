pipeline {
    agent any

    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['test', 'production'],
            description: 'Target environment'
        )

        string(
            name: 'PRODUCTION_BASE_URL',
            defaultValue: 'https://restful-booker.herokuapp.com/',
            description: 'Base URL for production environment'
        )
    }

    environment {
        ENVIRONMENT = "${params.ENVIRONMENT.toLowerCase()}"
        PRODUCTION_BASE_URL = "${params.PRODUCTION_BASE_URL}"
    }

    stages {

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    venv/bin/pip install --upgrade pip
                    venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    venv/bin/python -m pytest --alluredir=allure-results
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/allure-results/**', allowEmptyArchive: true
        }

        failure {
            echo 'The build failed!'
        }
    }
}

