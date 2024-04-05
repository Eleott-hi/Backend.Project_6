all: install grpc wait_for_it run

install:
	pip install -r requirements.txt

grpc:
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/auth/auth.proto

wait_for_it:
	./wait-for-it.sh -t 120 postgres_service:5432

run:
	python3 main.py

test:
	pytest
