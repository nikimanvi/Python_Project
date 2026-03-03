pipeline {
    agent any

    environment {
        // Docker Hub image name — replace with your Docker Hub username
        DOCKER_IMAGE     = "your-dockerhub-username/flask-python-app"
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
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running unit tests..."
                sh '''
                    . venv/bin/activate
                    pytest tests/ -v --tb=short
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
                sh "docker build -t ${DOCKER_VERSIONED} -t ${DOCKER_LATEST} ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "Pushing Docker image to Docker Hub..."
                sh '''
                    echo "$DOCKERHUB_CREDS_PSW" | docker login -u "$DOCKERHUB_CREDS_USR" --password-stdin
                    docker push ''' + "${DOCKER_VERSIONED}" + '''
                    docker push ''' + "${DOCKER_LATEST}" + '''
                '''
            }
        }

        stage('Cleanup') {
            steps {
                echo "Removing local Docker images to free space..."
                sh '''
                    docker rmi ''' + "${DOCKER_VERSIONED}" + ''' || true
                    docker rmi ''' + "${DOCKER_LATEST}" + ''' || true
                '''
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
            node {
                cleanWs()
            }
        }
    }
}
