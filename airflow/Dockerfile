# Use the official Apache Airflow image with Python 3.13 as the base image
FROM apache/airflow:3.3.0-python3.13

# Switch to the root user to install system packages and configure the image
USER root

# Add the user's local Python binaries to PATH so installed CLI tools are available
ENV PATH="/home/airflow/.local/bin:${PATH}"

# Define the cache directory used by uv (Python package manager)
ENV UV_CACHE_DIR=/home/airflow/.uv-cache

# Create the uv cache directory and grant ownership to the Airflow user (UID 50000)
RUN mkdir -p ${UV_CACHE_DIR} \
    && chown -R 50000:0 ${UV_CACHE_DIR}

# Install the PostgreSQL client, which is required for database administration
# and scripts that interact with PostgreSQL
RUN apt-get update \
    && apt-get install -y postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the Python dependency list into the image
COPY ./airflow/requirements.txt .

# Copy helper scripts into the Airflow scripts directory
COPY ./airflow/scripts /opt/airflow/scripts

# Copy the Meltano project into the Airflow container
COPY ./meltano-banvic/ /opt/airflow/meltano

# Convert Windows line endings (if present) in the database setup script,
# make it executable, and ensure the Meltano directory is executable
RUN sed -i 's/\r$//' /opt/airflow/scripts/create_banvic_db.sh \
    && chmod +x /opt/airflow/scripts/create_banvic_db.sh \
    && chmod +x /opt/airflow/meltano

# Switch back to the non-root Airflow user for security
USER airflow

# Install uv and upgrade pip using uv for faster dependency management
RUN pip install uv==0.11.29 \
    && uv pip install --upgrade pip

# Install all Python dependencies defined in requirements.txt without using a cache
RUN uv pip install --no-cache-dir -r requirements.txt