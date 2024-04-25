all: install grpc wait_for_it run

install:
	pip install -r requirements.txt

grpc:
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/auth/auth.proto

wait_for_it:
	chmod +x wait-for-it.sh
	./wait-for-it.sh -t 120 postgres_service:5432 -- \
	./wait-for-it.sh -t 120 auth_service:50051 -- \
	./wait-for-it.sh -t 120 redis_service:6379

run:
	python3 main.py