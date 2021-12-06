# USPTO Patent Fetcher

## How to run

1. Build CLI app and create necessary services

```bash
make dev
```

2. Run migrations

```bash
make migrate
```

3. Run an example command

```bash
make patent_fetcher FROM_DATE=2017-01-01 TO_DATE=2017-01-03
```

## How to run unit tests

```bash
make test
```

## Design decision & other considerations

- Used flask mainly as a way to give the code a scaffolding, but other good things come out of using it like
having decorators to build CLI apps 
- Went with Flask instead of Django because Django forces mgmt commands to be in a specific place in the code structure
which interferes with the intended code structure.
- A slightly-oriented Hexagonal architecture was used using 3 layers (Application - Domain - Infrastructure). 
- Used PostgreSQL because from the requirements given the data to store of a patent seemed mainly strings of short
length. No other requirements were given about the data to store but depending on things like data to be stored
are complete documents (patent body text) or the way the data is queried probably a different could be considered
like a document db.
- For the adapters the suffix acl was used which stands for anti-corruption layer. It was done as a way to mark that
data from an external source comes into the application and it's adapted to the domain.
- Only one test was written for the Command Controller. The following tests are important and they'd be written next:
  - for the http_patent_acl_adapter since this adapter includes the patent download progress logging and
  the mapping from the external USPTO data source to the domain of the patent fetcher application.
  - for the sqlalchemy_patent_repository since it maps from the domain objects to the data store entities.
