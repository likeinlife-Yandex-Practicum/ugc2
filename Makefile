up:
	docker compose up -d --build

down:
	docker compose down 

downv:
	docker compose down -v
	sudo rm -r ./docker_compose_files/mongodb/tmp


prod-up:
	docker compose -f docker-compose-prod.yaml up -d --build

prod-down:
	docker compose -f docker-compose-prod.yaml down -v

mongo-setup:
	sh ./mongo-setup.sh

freeze:
	poetry export >> requirements.txt