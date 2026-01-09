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
            description: 'Base URL for production'
        )
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
                    export ENVIRONMENT="${params.ENVIRONMENT}"
                    export PRODUCTION_BASE_URL="${params.PRODUCTION_BASE_URL}"

                    venv/bin/python -m pytest --alluredir=allure-results || true
                '''
            }
        }
    }

    post {
        always {
            allure([
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']]
            ])

            archiveArtifacts artifacts: '**/allure-results/**', allowEmptyArchive: true
        }
    }
}



