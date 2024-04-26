all: install wait_for_it run

install:
	pip install -r requirements.txt

wait_for_it:
	chmod +x wait-for-it.sh
	./wait-for-it.sh -t 120 postgres_service:5432 -- \
	./wait-for-it.sh -t 120 redis_service:6379

run:
	python3 main.py