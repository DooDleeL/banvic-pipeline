#!/usr/bin/env bash
set -euo pipefail

: "${POSTGRES_HOST:=postgres}"
: "${POSTGRES_PORT:=5432}"
: "${POSTGRES_USER:?POSTGRES_USER is required}"
: "${POSTGRES_PASSWORD:?POSTGRES_PASSWORD is required}"

export PGPASSWORD="${POSTGRES_PASSWORD}"

psql_opts=("-h" "${POSTGRES_HOST}" "-p" "${POSTGRES_PORT}" "-U" "${POSTGRES_USER}" "-v" "ON_ERROR_STOP=1")

echo "Checking for database \"banvic_warehouse\"..."
if ! psql "${psql_opts[@]}" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='banvic_warehouse'" | grep -q 1; then
  echo "Creating database banvic_warehouse..."
  psql "${psql_opts[@]}" -d postgres -c "CREATE DATABASE banvic_warehouse"
else
  echo "Database banvic_warehouse already exists."
fi

echo "Creating schema banvic in banvic_warehouse if missing..."
psql "${psql_opts[@]}" -d banvic_warehouse -c "CREATE SCHEMA IF NOT EXISTS banvic"

echo "Database and schema setup complete."
