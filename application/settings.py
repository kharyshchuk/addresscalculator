import os

DB_MONGO_NAME = os.environ.get('DB_MONGO_NAME', 'addresses')
DB_MONGO_HOST = os.environ.get('DB_MONGO_HOST', 'localhost')
DB_MONGO_PORT = os.environ.get('DB_MONGO_PORT', '27017')