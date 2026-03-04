pipeline {
    agent any

    environment {
        // Docker Hub image name — set to your namespace/repo on Docker Hub
        DOCKER_IMAGE     = "nikithamanvi/flask-python-app"
        DOCKER_TAG       = "${env.BUILD_NUMBER}"
        DOCKER_LATEST    = "${DOCKER_IMAGE}:latest"
        DOCKER_VERSIONED = "${DOCKER_IMAGE}:${DOCKER_TAG}"

        // Jenkins credential ID that stores Docker Hub username/password
        DOCKERHUB_CREDS  = credentials('docker-hub-credentials')
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Checking out source code..."
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing Python dependencies..."
                bat '''
                    py -m venv venv
                    call venv\\Scripts\\activate
                    py -m pip install --upgrade pip
                    py -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running unit tests..."
                bat '''
                    call venv\\Scripts\\activate && pytest tests/ -v --tb=short
                '''
            }
            post {
                always {
                    echo "Test stage complete."
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${DOCKER_VERSIONED}"
                bat "docker build -t ${DOCKER_VERSIONED} -t ${DOCKER_LATEST} ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "Pushing Docker image to Docker Hub..."
                bat """
                    echo %DOCKERHUB_CREDS_PSW% | docker login -u %DOCKERHUB_CREDS_USR% --password-stdin
                    docker push ${DOCKER_VERSIONED}
                    docker push ${DOCKER_LATEST}
                """
            }
        }

        stage('Cleanup') {
            steps {
                echo "Removing local Docker images to free space..."
                bat """
                    docker rmi ${DOCKER_VERSIONED} || exit /b 0
                    docker rmi ${DOCKER_LATEST} || exit /b 0
                """
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded! Image ${DOCKER_VERSIONED} pushed to Docker Hub."
        }
        failure {
            echo "Pipeline failed. Check the logs above for details."
        }
        always {
            echo "Cleaning up workspace..."
            cleanWs(cleanWhenNotBuilt: false,
                    deleteDirs: true,
                    disableDeferredWipeout: true,
                    notFailBuild: true)
        }
    }
}
