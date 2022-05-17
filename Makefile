start-stack:
	docker-compose up --build

test-backend:
	docker-compose run backend pytest --cov=api
	docker-compose rm -f
