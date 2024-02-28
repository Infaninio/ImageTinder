# Simple description of the webui


## Start docker database
```shell
docker run --detach --name regensbase --env MARIADB_ROOT_PASSWORD=password  mariadb:latest
```

## Get Docker IP
```shell
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' regensbase
```
