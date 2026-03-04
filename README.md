# Python Flask CI/CD (Jenkins)

## Pipeline flow (Jenkinsfile)
- Checkout: pulls source from Git.
- Install Dependencies: `py -m venv venv` then `py -m pip install -r requirements.txt`.
- Run Tests: activates venv and runs `pytest tests/ -v --tb=short`.
- Build Docker Image: builds and tags `${DOCKER_VERSIONED}` and `${DOCKER_LATEST}`.
- Push to Docker Hub: logs in with Jenkins credential `docker-hub-credentials` and pushes both tags to `nikithamanvi/flask-python-app`.
- Cleanup: removes local tags to save space.
- Post: `cleanWs` wipes workspace.

## Prereqs on Jenkins agent (Windows)
- Python installed for all users (so `py` launcher works from service account).
- Docker Desktop running and accessible to the Jenkins service user.
- Jenkins credential `docker-hub-credentials` set to Docker Hub username/password or PAT.

## Environment vars (Jenkinsfile)
- `DOCKER_IMAGE`: `nikithamanvi/flask-python-app`
- `DOCKER_TAG`: `${BUILD_NUMBER}`
- Tags pushed: `${DOCKER_IMAGE}:${DOCKER_TAG}` and `${DOCKER_IMAGE}:latest`
