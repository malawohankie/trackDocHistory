groovy_script = """
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
"""
# Write the Groovy script to a file
with open('Jenkinsfile.groovy', 'w') as file:
    file.write(groovy_script)

print("Groovy script has been written to Jenkinsfile.groovy")
