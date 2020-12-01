import asyncio
import json
from functools import wraps
from http.client import BAD_REQUEST

import pandas as pd
from flask import Flask, request, Response, abort

from constants import ALLOWED_EXTENSIONS, CLIENT_TYPE, INCORRECT_FILE_PARAMETER, FILE, INCORRECT_RESULT_ID_PARAMETER
from db_layers.mongo_db import db_mongo
from db_layers.result_repository import RESULT_ID
from helpers.helper import get_addresses_info

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# mongo = PyMongo(app)


@app.route('/')
def hello_world():
    return "Hello world!"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def async_action(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapped


@app.route('/getAddresses', methods=['POST'])
@async_action
async def get_addresses():
    files = request.files
    if len(files) == 0:
        abort(BAD_REQUEST, INCORRECT_FILE_PARAMETER)

    file = request.files[FILE]
    if not (file and allowed_file(request.files[FILE].filename)):
        abort(BAD_REQUEST, INCORRECT_FILE_PARAMETER)

    try:
        client_type = request.form[CLIENT_TYPE] if CLIENT_TYPE in request.form else None
        df = pd.read_csv(file)
        result = get_addresses_info(df, client_type)
        # db = mongo.db.test_database
        # collection = db['test-collection']
        # doc = collection.insert_one(result)
        await db_mongo.result_repository.save(result)

        return Response(json.dumps(result), mimetype="application/json", status=200)
    except Exception as exp:
        abort(BAD_REQUEST, f'Args: {exp.args}. Message: {exp}')


@app.route('/getResult', methods=['GET'])
@async_action
async def get_result():
    if RESULT_ID not in request.args:
        abort(BAD_REQUEST, INCORRECT_RESULT_ID_PARAMETER)

    result_id = request.args.get(RESULT_ID)
    try:
        result = await db_mongo.result_repository.find_one(result_id=result_id, without_id=True)
        return Response(json.dumps(result), mimetype="application/json", status=200)
    except Exception as exp:
        abort(BAD_REQUEST, f'Args: {exp.args}. Message: {exp}')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
