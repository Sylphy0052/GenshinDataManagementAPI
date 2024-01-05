#!/bin/bash

image_name=my-app
container_name=task_management_api

docker stop $container_name && docker rm $container_name && docker rmi $image_name
docker build -t $image_name .
# docker run -p 80:80 -d --name $container_name --privileged $image_name:latest
docker run -p 80:80 -v ./app:/app -itd --name $container_name --privileged $image_name:latest
docker exec -it $container_name /bin/bash
