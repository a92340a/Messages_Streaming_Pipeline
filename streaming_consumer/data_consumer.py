import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructField, StructType, StringType, DateType, TimestampType, BooleanType
import psycopg2


BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS", "kafka-service:9092")
TOPIC = os.getenv("TOPIC", "message_data")

POSTGRES_DBNAME = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")


spark = (
    SparkSession.builder.appName("KafkaStreaming")
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1")
    .config("spark.executor.memory", "2g")
    .config("spark.executor.cores", "1")
    .getOrCreate()
)
spark.conf.set("spark.sql.shuffle.partitions", 5)  # for local machine


# subscribe from Kafka
df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS)
    .option("subscribe", TOPIC)
    .option("startingOffsets", "earliest")  # latest
    .load()
)

# decode the value of Kafka message, and convert into string
df_value = df.selectExpr("CAST(value AS STRING)")
json_schema = (
    StructType()
    .add("id", StringType())
    .add("message_id", StringType())
    .add("campaign_id", StringType())
    .add("message_type", StringType())
    .add("client_id", StringType())
    .add("channel", StringType())
    .add("category", StringType())
    .add("platform", StringType())
    .add("email_provider", StringType())
    .add("stream", StringType())
    .add("date", DateType())
    .add("sent_at", TimestampType())
    .add("is_opened", BooleanType())
    .add("opened_first_time_at", TimestampType())
    .add("opened_last_time_at", TimestampType())
    .add("is_clicked", BooleanType())
    .add("clicked_first_time_at", TimestampType())
    .add("clicked_last_time_at", TimestampType())
    .add("is_unsubscribed", BooleanType())
    .add("unsubscribed_at", TimestampType())
    .add("is_hard_bounced", BooleanType())
    .add("hard_bounced_at", TimestampType())
    .add("is_soft_bounced", BooleanType())
    .add("soft_bounced_at", TimestampType())
    .add("is_complained", BooleanType())
    .add("complained_at", TimestampType())
    .add("is_blocked", BooleanType())
    .add("blocked_at", TimestampType())
    .add("is_purchased", BooleanType())
    .add("purchased_at", TimestampType())
    .add("created_at", TimestampType())
    .add("updated_at", TimestampType())
)
df_decode = df_value.select(from_json(col("value"), json_schema).alias("data")).select("data.*")

df_cleaned = df_decode.filter(col("message_id").isNotNull()).drop(
    "category",
    "stream",
    "is_hard_bounced",
    "hard_bounced_at",
    "is_soft_bounced",
    "soft_bounced_at",
    "is_blocked",
    "blocked_at",
)


def write_to_postgres(batch_df, batch_id):
    connection = None
    try:
        connection = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DBNAME,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        )
        cursor = connection.cursor()

        for row in batch_df.rdd.collect():
            insert_query = """
            INSERT INTO messages (id, message_id, campaign_id, message_type, client_id, channel, platform, email_provider, date, sent_at, is_opened, opened_first_time_at, opened_last_time_at, is_clicked, clicked_first_time_at, clicked_last_time_at, is_unsubscribed, unsubscribed_at, is_complained, complained_at, is_purchased, purchased_at, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                insert_query,
                (
                    row.id,
                    row.message_id,
                    row.campaign_id,
                    row.message_type,
                    row.client_id,
                    row.channel,
                    row.platform,
                    row.email_provider,
                    row.date,
                    row.sent_at,
                    row.is_opened,
                    row.opened_first_time_at,
                    row.opened_last_time_at,
                    row.is_clicked,
                    row.clicked_first_time_at,
                    row.clicked_last_time_at,
                    row.is_unsubscribed,
                    row.unsubscribed_at,
                    row.is_complained,
                    row.complained_at,
                    row.is_purchased,
                    row.purchased_at,
                    row.created_at,
                    row.updated_at,
                ),
            )
        connection.commit()
    except Exception as e:
        print(f"Error writing to PostgreSQL: {e}")
    finally:
        if connection:
            connection.close()


# write to PostgreSQL
# query = df_cleaned.writeStream.format("console").outputMode("append").start()
query = df_cleaned.writeStream.foreachBatch(write_to_postgres).outputMode("append").start()


query.awaitTermination()
