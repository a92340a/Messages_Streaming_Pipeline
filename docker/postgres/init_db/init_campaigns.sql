
-- create table schema
CREATE TABLE campaigns (
    id VARCHAR(10) NOT NULL,
    campaign_type VARCHAR(20),
    channel VARCHAR(20),
    topic VARCHAR(50),
    started_at TIMESTAMP,
    finished_at TIMESTAMP,
    total_count INTEGER,
    ab_test BOOLEAN,
    warmup_mode BOOLEAN,
    hour_limit INTEGER,
    subject_length NUMERIC,
    subject_with_personalization BOOLEAN,
    subject_with_deadline BOOLEAN,
    subject_with_emoji BOOLEAN,
    subject_with_bonuses BOOLEAN,
    subject_with_discount BOOLEAN,
    subject_with_saleout BOOLEAN,
    is_test BOOLEAN,
    position INTEGER
);

-- import CSV file
COPY campaigns(id,campaign_type,channel,topic,started_at,finished_at,total_count,ab_test,warmup_mode,hour_limit,subject_length,subject_with_personalization,subject_with_deadline,subject_with_emoji,subject_with_bonuses,subject_with_discount,subject_with_saleout,is_test,position)
FROM '/docker-entrypoint-initdb.d/campaigns.csv'
DELIMITER ','
CSV HEADER
NULL AS '';

