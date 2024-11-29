# Microservices Demo

Simple microservices system with User Service and Order Service.

## Prerequisites
- Docker
- Docker Compose

## Setup
1. Clone the repository
2. Start Docker:
```bash
sudo systemctl start docker
```

3. Build and run:
```bash
docker compose up -d
```

## Test the Services

### Create a User
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"name":"Mario Rossi","email":"mario@example.com"}' \
  http://localhost:5000/users
```

### Create an Order
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"user_id":"1","items":["pizza"],"total":10.50}' \
  http://localhost:5001/orders
```

### Check Services Status
```bash
docker ps
```

### View Logs
```bash
docker compose logs
```

### Stop Services
```bash
docker compose down
```