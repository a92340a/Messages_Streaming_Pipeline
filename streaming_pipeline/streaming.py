from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
import os
from config import TOPIC

os.environ["PYSPARK_SUBMIT_ARGS"] = (
    "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1,org.apache.spark:spark-avro_2.12:3.3.1 pyspark-shell"
)

# 設定 GCS 服務帳戶金鑰
credentials_location = "./docker/mage/google-cred.json"
gcs_bucket_path = "gs://messages-streaming-project-data/"

# 初始化 SparkSession，直接使用 packages 參數下載依賴
spark = (
    SparkSession.builder.appName("KafkaStreaming")
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1," "com.google.cloud.bigdataoss:gcs-connector:hadoop3-2.2.5",
    )
    .config("spark.hadoop.google.cloud.auth.service.account.enable", "true")
    .config("spark.hadoop.google.cloud.auth.service.account.json.keyfile", credentials_location)
    .getOrCreate()
)

# 讀取 Kafka 資料
df_raw_stream = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092,broker:29092")
    .option("subscribe", TOPIC)
    .option("startingOffsets", "earliest")
    .option("checkpointLocation", "checkpoint")
    .load()
)

# JSON 解析與型別轉換# 進行 ETL 處理
transformed_df = df.selectExpr("CAST(value AS STRING)").filter("<condition>")


json_schema = (
    "module_name string, module_id string, email string, time_homework string, time_lectures string, score string"
)
df_parsed = (
    df_raw_stream.withColumn("value_str", df_raw_stream["value"].cast("string"))
    .select(from_json(col("value_str"), json_schema).alias("data"))
    .select("data.*")
)


# 批次寫入 GCS
def write_to_gcs(df, batch_id, path):
    output_path = f"{gcs_bucket_path}streaming_data/{path}/batch_{batch_id}/"
    df.write.format("parquet").mode("overwrite").save(output_path)


# 將結果寫入 PostgreSQL
transformed_df.writeStream.format("jdbc").option(
    "url", "jdbc:postgresql://<postgres-vm-internal-ip>:5432/db_name"
).option("dbtable", "sales_table").option("user", "username").option("password", "password").start()

# 定義 streaming query
query = df_parsed.writeStream.foreachBatch(lambda df, batch_id: write_to_gcs(df, batch_id, "fact_score")).start()


query.awaitTermination()
