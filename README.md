# Geo-Kafka-Clickhouse

## Goals
This project is just an experiment to tinker with Apache Kafka, Fastapi and Clickhouse with a geographic twist.

The goal is to create a scalable, full event processor and aggregator for geospatial data with as little code as possible (less than 75 lines!).

## Requirements
 - Docker
 - Docker-compose

## Install
Execute
```
docker-compose up
```

## Run tests
Execute
```
docker-compose run api python3 -m unittest src.test.test_main
```

## API documentation

### Put events:
Perform a `POST` operation on http://localhost:8000/put_event with the following parameters:
 - `latitude`: The latitude of the event.
 - `longitude`: The longitude of the event.
 - `mname`: The name of the measurement.
 - `mvalue`: The value of the measurement.
 - `timestamp` (optional): The timestamp of the measurement (the current timestamp will be used if this parameter is not present).

Why `POST` instead of `PUT`? Because `GET` and `POST` are widely implemented but `PUT` may not (in the past for example I found a REST implementation for Unity3D that could only perform `GET` and `POST` requests).

For convenience, a `GET` request is also set up. Example: http://localhost:8000/put_event?latitude=40.419903&longitude=-3.705793&mname=temperature&mvalue=26.1

### Get aggregations
Perform a `GET` operation on http://localhost:8000/get_aggregation with the following parameters:
 - `polygon` (optional): A polygon with the format `[(longitude1,latitude1), ..., (longitudeN,latitudeN)]`.
 - `mname` (optional): The name of the measurement to aggregate.
 - `timestamp_ini` (optional): The initial timestamp to filter.
 - `timestamp_end` (optional): The end timestamp to filter.
 - `aggregation`: The desired aggregation to perform (`avg` by default).

Example: http://localhost:8000/get_aggregation?mname=temperature&polygon=[(-3.706114,%2040.420363),%20(-3.705434,%2040.420350),%20(-3.705540,%2040.419558),%20(-3.706123,%2040.419580)]

### TL;DR;
Thanks to Fastapi the documentation can be accessed via http://localhost:8000/docs (once the project is started)

## Uninstall
Stop everything doing:
```
docker-compose down
```

You can remove all the volumes created executing:
```
docker volume rm gkch_clickhouse-data
docker volume rm gkch_kafka-data
docker volume rm gkch_kafka-etc
docker volume rm gkch_zk-data
docker volume rm gkch_zk-logs
```

You can remove the images created executing:
```
docker rmi gkch_api:latest
docker rmi gkch_clickhouse:latest
```

Take a look at the rest of your installed images (executing `docker image ls`) as you may also want to remove the following images:
```
docker rmi confluentinc/cp-enterprise-control-center:7.3.0
docker rmi confluentinc/cp-kafka:7.3.0
docker rmi confluentinc/cp-zookeeper:7.3.0
docker rmi yandex/clickhouse-server:21.3.20.1
```

## TO DOs
 - Improve the API (more parameters, validations, documentation, error handling, ...).
 - Add more consumers (Portgres for example).
 - Add more tests.
 - Remove `--reload` from `command` section in the `api` service within the `docker-compose.yml` file if you want to use this in a production environment.
 - Consider removing the `control-center` if you want to use this in a production environment (it's great for debugging).

## Caveats
Do not use this in a production environment. This is just an experiment to play with Kafka, Fastapi and Clickhouse created on a rainy fall afternoon.

## LICENSE
Apache License 2.0
