DB_CONTAINER_NAME := postgres_service

all: clean_db copy_proto up

up:
	docker-compose up

down:
	docker-compose down

clean_db:
	-docker stop $(DB_CONTAINER_NAME)
	-docker rm $(DB_CONTAINER_NAME)

copy_proto:
	cp proto/auth.proto auth_service/proto/auth/auth.proto
	cp proto/auth.proto store_service/proto/auth/auth.proto

prune:
	docker system prune -a
