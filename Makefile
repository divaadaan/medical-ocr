.PHONY: help build run stop clean test lint format

help:
	@echo "Available commands:"
	@echo "  make build   - Build Docker image"
	@echo "  make run     - Run application with Docker Compose"
	@echo "  make stop    - Stop running containers"
	@echo "  make clean   - Remove containers and images"
	@echo "  make test    - Run tests"
	@echo "  make lint    - Run linting checks"
	@echo "  make format  - Format code with black"

build:
	docker-compose build

run:
	docker-compose up

run-detached:
	docker-compose up -d

stop:
	docker-compose down

clean:
	docker-compose down -v --rmi all

test:
	pytest tests/ -v

lint:
	black --check app/ tests/

format:
	black app/ tests/

dev:
	python -m app.main

install:
	pip install -r requirements.txt
