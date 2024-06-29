# Build the docker container
sudo docker build -t dns-updater .

# Run the docker container (without persistance)
# sudo docker run --env-file .env dns-updater

# Run the docker container (with persistance - even on reboot)
sudo docker run -d --restart unless-stopped --env-file .env dns-updater
