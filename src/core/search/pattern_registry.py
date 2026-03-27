def get_default_patterns():
    return {
        "SQL_ERROR": r'java\.sql\.SQLException',
        "CONNECTION": r'connection.*failed',
        "NULL_POINTER": r'NullPointerException',
    }