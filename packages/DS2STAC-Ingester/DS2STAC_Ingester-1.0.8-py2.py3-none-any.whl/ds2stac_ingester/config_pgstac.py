import os

variabl_list = [
    ["APP_HOST", "0.0.0.0"],
    ["APP_PORT", "8082"],
    ["RELOAD", "true"],
    ["ENVIRONMENT", "local"],
    ["POSTGRES_USER", "hadizadeh-m"],
    ["POSTGRES_PASS", ""],
    ["POSTGRES_DBNAME", "postgis"],
    ["POSTGRES_HOST_READER", "localhost"],
    ["POSTGRES_HOST_WRITER", "localhost"],
    ["POSTGRES_PORT", "5432"],
    ["WEB_CONCURRENCY", "10"],
    ["VSI_CACHE", "TRUE"],
    ["GDAL_HTTP_MERGE_CONSECUTIVE_RANGES", "YES"],
    ["GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR"],
    ["DB_MIN_CONN_SIZE", "1"],
    ["DB_MAX_CONN_SIZE", "10"],
    ["USE_API_HYDRATE", "${USE_API_HYDRATE:-false}"],
    ["POSTGRES_USER", "hadizadeh-m"],
    ["POSTGRES_PASSWORD", ""],
    ["POSTGRES_DB", "postgis"],
    ["PGUSER", "hadizadeh-m"],
    ["PGPASSWORD", ""],
    ["PGHOST", "localhost"],
    ["PGDATABASE", "postgis"],
]


# Define all variabels as an array and for-loop over the array
def run_all():
    for i in variabl_list:
        if os.getenv(i[0]) is None:
            os.environ[i[0]] = i[1]
