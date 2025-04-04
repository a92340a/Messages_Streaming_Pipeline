FROM bitnami/spark:3.3.1

# use root
USER root

# Install Python 3.11 and related tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.9 \
    python3.9-venv \
    python3.9-distutils \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1 \
    && curl -sS https://bootstrap.pypa.io/get-pip.py | python3

# Install Python packages
RUN pip install --no-cache-dir pyspark==3.3.1 psycopg2-binary==2.9.6 python-dotenv

# Switch to not-root user
USER 1001
