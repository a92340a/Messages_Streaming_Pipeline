

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