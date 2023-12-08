test:
	docker compose up --abort-on-container-exit --exit-code-from tests --attach tests

dev:
	docker compose up --build --attach tests

down:
	docker compose down

downv:
	docker compose down -v

freeze:
	poetry export -o requirements.txt