
pipeline {
    agent any
    environment {
        PYTHON_VERSION = 'python3'
    }
    stages {
        stage('version') {
            steps {
                script {
                    sh "\${PYTHON_VERSION} --version"
                }
            }
        }
        stage('hello') {
            steps {
                script {
                    sh "\${PYTHON_VERSION} hello.py"
                }
            }
        }
    }
}
