# Use docker-compose.yml to build the app
FROM docker/compose:latest

WORKDIR /app
COPY . .

CMD ["docker-compose", "up", "--build"]