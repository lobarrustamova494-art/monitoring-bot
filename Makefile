.PHONY: help build up down logs restart clean test

help:
	@echo "Available commands:"
	@echo "  make build    - Build Docker images"
	@echo "  make up       - Start all services"
	@echo "  make down     - Stop all services"
	@echo "  make logs     - Show logs"
	@echo "  make restart  - Restart bot service"
	@echo "  make clean    - Remove all containers and volumes"
	@echo "  make test     - Run tests"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f bot

restart:
	docker-compose restart bot

clean:
	docker-compose down -v
	docker system prune -f

test:
	pytest tests/ -v

migrate:
	docker-compose exec bot alembic upgrade head

migration:
	docker-compose exec bot alembic revision --autogenerate -m "$(msg)"
