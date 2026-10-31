pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Run Tests with Docker Compose') {
            steps {
                sh '''
                    # 1. Spin up the containers defined in docker-compose.yml
                    docker compose up --build -d

                    # 2. Execute pytest inside the already running 'app' container
                    docker compose exec -T app pytest --junitxml=test-reports/results.xml

                    # 3. Copy the test report out of the container if needed, or map it via volumes
                    docker cp messaging_app_backend:/app/test-reports ./test-reports
                '''
            }
        }
    }

    post {
        always {
            // Publishes test results
            junit 'test-reports/results.xml'

            // Shut down and clean up containers after tests finish
            sh 'docker compose down -v'
        }
    }
}