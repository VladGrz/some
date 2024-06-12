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

                    // Create a network if it doesn't exist
                    sh 'docker network create weather-net || true'

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
                        if [ \$(docker ps -aq -f name=node-exporter) ]; then
                            docker stop node-exporter
                            docker rm node-exporter
                        fi
                        if [ \$(docker ps -aq -f name=cadvisor) ]; then
                            docker stop cadvisor
                            docker rm cadvisor
                        fi
                    """

                    weatherImage.run("--network weather-net -d -p 8000:8000 --name weather-bot-container --label app=weather-bot -e API_TOKEN=${API_TOKEN} -e WEATHER_API_KEY=${WEATHER_API_KEY}")

                    sh """
                        docker run -d --network weather-net \
                            --name prometheus \
                            -p 9090:9090 \
                            -v \${PWD}/prometheus.yml:/etc/prometheus/prometheus.yml \
                            prom/prometheus
                    """

                    sh """
                        docker run -d --network weather-net \
                            --name grafana \
                            -p 3000:3000 \
                            -v \$(PWD)/provisioning/datasources:/etc/grafana/provisioning/datasources \
                            -v \$(PWD)/provisioning/dashboards:/etc/grafana/provisioning/dashboards \
                            -v \$(PWD)/dashboards:/var/lib/grafana/dashboards \
                            grafana/grafana
                    """

                    sh """
                        docker run -d --network weather-net \
                            --name node-exporter \
                            -p 9100:9100 \
                            prom/node-exporter
                    """

                    sh """
                        docker run -d --network weather-net \
                            --name cadvisor \
                            -p 8081:8080 \
                            -v /:/rootfs:ro \
                            -v /var/run:/var/run:ro \
                            -v /sys:/sys:ro \
                            -v /var/lib/docker/:/var/lib/docker:ro \
                            gcr.io/cadvisor/cadvisor:v0.47.0
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
