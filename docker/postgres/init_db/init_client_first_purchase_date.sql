-- create table schema
CREATE TABLE client_first_purchase_date (
    client_id VARCHAR(20) NOT NULL,
    first_purchase_date DATE NOT NULL
);

-- import CSV file
COPY client_first_purchase_date(client_id, first_purchase_date)
FROM '/docker-entrypoint-initdb.d/client_first_purchase_date.csv'
DELIMITER ','
CSV HEADER;
