pipeline {
    agent any

    environment {
        API_TOKEN = credentials('API_TOKEN')
        WEATHER_API_KEY = credentials('WEATHER_API_KEY')
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/VitaliyKuz/prikm-bot-cursach.git'
            }
        }

        stage('Build and Run Docker Container') {
            steps {
                script {
                    def image = docker.build("weather-bot-image")
                    image.run('-d -p 5000:5000 -p 8000:8000 --name weather-bot-container', 
                      "--env API_TOKEN=${API_TOKEN} --env WEATHER_API_KEY=${WEATHER_API_KEY}")
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
