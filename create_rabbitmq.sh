#!/bin/sh
# RabbitMQ в Docker: AMQP localhost:5672, веб-интерфейс http://localhost:15672 (guest / guest)
docker run --name rabbitmq -p 5672:5672 -p 15672:15672 -d rabbitmq:3-management
