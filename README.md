# Task Manager API

## Installation
1. Create .env
`cp .env.example .env`
2. Provide necessary setup to .env
3. Build the docker image
`docker build -t taskmanagerapi .`
4. Run docker container
`docker run -p 5000:5000 taskmanagerapi`
5. Access the application

## Remove docker container 
`docker rm taskmanagerapi`