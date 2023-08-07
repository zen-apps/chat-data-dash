DOCKERFILE := Dockerfile-local
APP_NAME := dash_dev_app
APP_PORT := 7777

stop:
	docker stop ${APP_NAME} && docker rm -f ${APP_NAME} || true

build: stop
	docker build -f ${DOCKERFILE} -t ${APP_NAME}:latest .

up: stop build
	docker run -d -p ${APP_PORT}:3457 -v ${PWD}:/usr/src/app --env-file dash_app/config/dev_sample.env --name ${APP_NAME} ${APP_NAME}:latest 

logs: up
	docker logs ${APP_NAME} --tail 100 -f