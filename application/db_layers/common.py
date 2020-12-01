from settings import DB_MONGO_NAME, DB_MONGO_HOST, DB_MONGO_PORT


def get_name_db():
    return DB_MONGO_NAME


# MONGO_URI = os.environ.get('MONGO_URI', "mongodb://localhost:27017/myDatabase")
def create_uri(scheme=None, host=None, port=None, db_name=None):
    return f'{scheme}://{host}:{port}/{db_name}'


def get_mongo_connect_string():
    return create_uri(
        scheme='mongodb',
        host=DB_MONGO_HOST,
        port=DB_MONGO_PORT,
        db_name=DB_MONGO_NAME
    )
