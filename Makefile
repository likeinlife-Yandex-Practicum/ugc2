up:
	docker compose up -d --build

down:
	docker compose down 

downv:
	docker compose down -v

mongo-setup:
	sh ./mongo-setup.sh

freeze:
	poetry export -o src/requirements.txt --without-hashes