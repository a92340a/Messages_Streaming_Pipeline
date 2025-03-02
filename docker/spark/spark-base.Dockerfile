FROM bitnami/spark:latest

# use root
USER root

# Install Python 3.11 and related tools
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3.11-distutils \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
    && curl -sS https://bootstrap.pypa.io/get-pip.py | python3

# Install Python packages
RUN pip install --no-cache-dir pyspark psycopg2-binary python-dotenv

# Switch to not-root user
USER 1001
