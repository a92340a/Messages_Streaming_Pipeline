# -- Software Stack Version
SPARK_VERSION="3.3.1"
HADOOP_VERSION="3"

# -- Building the Images

docker build \
  -f "spark-base.Dockerfile" \
  -t spark-base .

docker build \
  -f "spark-master.Dockerfile" \
  -t spark-master .

docker build \
  -f "spark-worker.Dockerfile" \
  -t spark-worker .