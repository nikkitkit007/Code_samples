
# Rabbitmq
______
## Main info
1. For connect to rabbitmq's port 15672 you need connect to rabbitmq container ```docker-compose exec rabbitmq bash```,
and then run ```rabbitmq-plugins enable rabbitmq_management```
2. ...

______
## Interesting moments

Rabbit's consumers default receive messages in one queue by order. It can help to parallel your tasks.
