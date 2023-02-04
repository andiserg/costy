pipeline {
    agent none
    stages {
        stage('Build') {
            agent {
                docker {
                    image 'python:3.10'
                }
            }
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python -m -t pytest'
            }
        }
    }
}
