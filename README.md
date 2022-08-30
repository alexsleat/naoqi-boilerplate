# Config:
Edit docker_config to include names, etc

# Build:
docker build -t sanne_presentation22 .

# Create / run container:
./run_docker.sh

# Run container:
. attach_docker.sh


# Run example code:
python say_something.py --ip 192.168.100.21