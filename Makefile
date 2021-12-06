.PHONY: tests

# Usage: make dev
dev:
	export SQLALCHEMY_DATABASE_URI=postgresql://patentfetcherdbuser:password@host.docker.internal:5432/patentfetcherdb
	docker build -t patent-fetcher -f deploy/docker/Dockerfile .
	docker-compose -f docker-compose.yml up --build

# Usage: make destroy
destroy:
	docker-compose -f docker-compose.yml down

# Usage: make migrate
migrate:
	docker run --rm -it -e SQLALCHEMY_DATABASE_URI=postgresql://patentfetcherdbuser:password@host.docker.internal:5432/patentfetcherdb -e FLASK_APP=src.app.py -e FLASK_DEBUG=1 --name patent_fetcher patent-fetcher:latest flask db upgrade

# Usage: make test
test:
	docker exec -i localdb psql -U patentfetcherdbuser -c "DROP DATABASE IF EXISTS patentfetcherdb;" postgres;
	docker exec -i localdb psql -U patentfetcherdbuser -c "CREATE DATABASE patentfetcherdb;" postgres;
	docker build -t patent-fetcher -f deploy/docker/Dockerfile .
	docker run --rm -it -e SQLALCHEMY_DATABASE_URI=postgresql://patentfetcherdbuser:password@host.docker.internal:5432/patentfetcherdb -e FLASK_APP=src.app.py -e FLASK_DEBUG=1 --name patent_fetcher patent-fetcher:latest flask db upgrade
	docker run --rm -it -e SQLALCHEMY_DATABASE_URI=postgresql://patentfetcherdbuser:password@host.docker.internal:5432/patentfetcherdb -e FLASK_APP=src.app.py -e FLASK_DEBUG=1 --name patent_fetcher patent-fetcher:latest pytest -vvv tests/

# Usage: make patent_fetcher FROM_DATE=2017-01-01 TO_DATE=2017-01-03
patent_fetcher:
	docker run --rm -it -e SQLALCHEMY_DATABASE_URI=postgresql://patentfetcherdbuser:password@host.docker.internal:5432/patentfetcherdb -e FLASK_APP=src.app.py -e FLASK_DEBUG=1 --name patent_fetcher patent-fetcher:latest flask patents patents $(FROM_DATE) $(TO_DATE)