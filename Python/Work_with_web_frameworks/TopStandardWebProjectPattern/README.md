## Quiq start

1) build & start docker-compose 

``docker-compose up``

2) make db migration

``alembic upgrade head``


___

## Extra commands

### Create revision of migration

``alembic revision --autogenerate -m "<revision_description>"``

