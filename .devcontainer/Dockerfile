FROM mcr.microsoft.com/devcontainers/python:3.11

RUN pip install --no-cache-dir \
    dbt-duckdb==1.9.1 \
    faker==33.3.1 \
    numpy==2.2.3

# Install DuckDB CLI
RUN wget -qO /tmp/duckdb.zip https://github.com/duckdb/duckdb/releases/download/v1.2.2/duckdb_cli-linux-amd64.zip \
    && unzip /tmp/duckdb.zip -d /usr/local/bin \
    && chmod +x /usr/local/bin/duckdb \
    && rm /tmp/duckdb.zip

# Create dbt profiles directory
RUN mkdir -p /home/vscode/.dbt
