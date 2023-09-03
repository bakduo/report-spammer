build:
	docker build -t spamapp:1.0.0 .

clean:
	docker rmi spamapp:1.0.0
	
clean-image-psql:
	docker compose -f compose-psql down
	docker rmi spamapp:1.0.0

clean-image-sql:
	docker compose -f compose-sql down
	docker rmi spamapp:1.0.0

run-psql:
	docker compose -f compose-psql.yaml up

rundb-postgres:
	docker compose -f onlydb-postgres.yaml up

downdb-postgres:
	docker compose -f onlydb-postgres.yaml down

rundb-mariadb:
	docker compose -f onlydb-mariadb.yaml up

downdb-mariadb:
	docker compose -f onlydb-mariadb.yaml down
	
down-psql:
	docker compose -f compose-psql.yaml down

down-sql:
	docker compose -f compose-sql.yaml down

generate-requirements:
	pipenv lock && pipenv requirements > requirements.txt