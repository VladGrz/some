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

        stage('Build and Run Docker Containers') {
            steps {
                script {
                    def weatherImage = docker.build("weather-bot-image")

                    // Stop and remove the existing containers if they exist
                    sh """
                        if [ \$(docker ps -aq -f name=weather-bot-container) ]; then
                            docker stop weather-bot-container
                            docker rm weather-bot-container
                        fi
                        if [ \$(docker ps -aq -f name=prometheus) ]; then
                            docker stop prometheus
                            docker rm prometheus
                        fi
                        if [ \$(docker ps -aq -f name=grafana) ]; then
                            docker stop grafana
                            docker rm grafana
                        fi
                    """

                    // Run WeatherBot container with a label
                    weatherImage.run("-d -p 8000:8000 --name weather-bot-container --label app=weather-bot -e API_TOKEN=${API_TOKEN} -e WEATHER_API_KEY=${WEATHER_API_KEY}")

                    // Run Prometheus container
                    sh """
                        docker run -d \
                            --name prometheus \
                            -p 9090:9090 \
                            -v /home/vboxuser/prikm-bot-cursach/prometheus.yml:/etc/prometheus/prometheus.yml \
                            prom/prometheus
                    """

                    // Run Grafana container
                    sh """
                        docker run -d \
                            --name grafana \
                            -p 3000:3000 \
                            grafana/grafana
                    """
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
