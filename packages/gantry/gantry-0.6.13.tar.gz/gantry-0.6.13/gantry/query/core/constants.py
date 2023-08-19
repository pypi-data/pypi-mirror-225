TIMEZONE = {"TO_TIMEZONE": "UTC"}

SCHEMA_TYPES = [
    "prediction_datanodes",
    "feedback_datanodes",
    "projection_datanodes",
]

DEFAULT_FETCH_BATCH_SIZE = (
    20480  # Optimized for https://druid.apache.org/docs/latest/querying/scan-query
)
