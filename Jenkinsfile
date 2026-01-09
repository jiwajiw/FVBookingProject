pipeline {
    agent any

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

        failure {
            echo 'The build failed!'
        }
    }
}


