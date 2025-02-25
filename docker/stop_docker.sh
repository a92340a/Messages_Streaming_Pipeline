# Function to stop containers
stop_containers() {
    echo "Closing $1 related containers"
    docker-compose -f "$2" down
    echo
}

# Stop containers
stop_containers "Postgres" "./postgres/docker-compose.yml"
stop_containers "Kafka" "./kafka/docker-compose.yml"
stop_containers "Spark" "./spark/docker-compose.yml"

echo "Closed all containers."