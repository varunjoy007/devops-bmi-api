pipeline {
    agent any
    stages {
        stage('Setup Environment') {
            steps {
                sh 'python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Run Automated Tests') {
            steps {
                sh '. venv/bin/activate && pytest -v'
            }
        }
        stage('Package Build Artifact') {
            steps {
                sh 'tar -czf bmi-api-build-${BUILD_NUMBER}.tar.gz app.py requirements.txt'
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: '*.tar.gz', fingerprint: true
        }
    }
}
