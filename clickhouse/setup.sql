CREATE TABLE IF NOT EXISTS queue (
    timestamp UInt64,
    latitude Float32,
    longitude Float32,
    mname String,
    mvalue Float32
) ENGINE = Kafka('kafka:9092', 'gkch', 'group1', 'JSONEachRow');

CREATE TABLE IF NOT EXISTS measurements (
    timestamp UInt64,
    latitude Float32,
    longitude Float32,
    mname String,
    mvalue Float32
) ENGINE = MergeTree()
PRIMARY KEY (latitude, longitude, mname, timestamp)
ORDER BY (latitude, longitude, mname, timestamp)
SETTINGS index_granularity = 8192, index_granularity_bytes = 0;

CREATE MATERIALIZED VIEW IF NOT EXISTS consumer TO measurements
AS SELECT timestamp, latitude, longitude, mname, mvalue FROM queue;
