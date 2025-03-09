-- create table schema
CREATE TABLE holidays (
    date DATE NOT NULL,
    holiday VARCHAR(50) NOT NULL
);

-- import CSV file
COPY holidays(date, holiday)
FROM '/mnt/gcs/holidays.csv'
DELIMITER ','
CSV HEADER;
