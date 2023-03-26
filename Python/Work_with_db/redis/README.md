# Redis
## Инструкция по запуску

Находясь в корне репозитория, выполнить команду:
* `docker-compose up`

Если контейнер с Redis выдал предупреждение, то исполните команду ниже (встретил на ubuntu):
* ```echo "vm.overcommit_memory = 1" | sudo tee /etc/sysctl.d/nextcloud-aio-memory-overcommit.conf```

https://github.com/nextcloud/all-in-one/discussions/1731

Для подключения к redis:
* ```docker exec -it telegram-our_bot_redis_1 redis-cli```
