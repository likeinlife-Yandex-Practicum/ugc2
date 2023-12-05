up:
	docker compose up -d --build

down:
	docker compose down 

downv:
	docker compose down -v
	sudo rm -r ./docker_compose_files/mongodb/tmp

mongo-setup:
	sh ./mongo-setup.sh

freeze:
	poetry export >> requirements.txt