import json
import socket
import logging
import logging.config
from pymongo import MongoClient
from flask import Flask, request

app = Flask(__name__)

mongo = MongoClient(host='mongo_db')
table = mongo['databases']['cache']

cache = {}

logging.config.fileConfig('log.conf')


@app.route('/post', methods=['POST'])
def post():
    try:
        req = json.loads(request.data.decode('utf-8'))
    except:
        code = 400
        return '', code

    if table.find_one({'key': req['key']}) is None:
        table.insert_one({'key': req['key'], 'value': req['message']})
        code = 200
        tmp = json.dumps({"status": "Create"})
        return tmp.encode("utf-8"), code
    else:
        code = 208
        tmp = json.dumps({"status": "Already Created"})
        return tmp.encode("utf-8"), code


@app.route('/put', methods=['PUT'])
def put():
    try:
        req = json.loads(request.data.decode('utf-8'))
    except:
        code = 400
        return '', code

    table.find_one_and_update(
        {'key':req['key']}, {"$set": {'key':req['key'], 'value': req['message']}}, upsert=True
    )
    code = 200
    return '', code


@app.route('/delete', methods=['DELETE'])
def delete():
    try:
        req = json.loads(request.data.decode('utf-8'))
    except:
        code = 400
        return '', code

    if table.find_one({'key': req['key']}) is not None:
        if req['key'] in cache.keys():
            del cache[req['key']]
        table.delete(req['key'])
    code = 205
    return '', code


@app.route('/get', methods=['GET'])
def get():
    try:
        req = json.loads(request.data.decode('utf-8'))
    except:
        code = 400
        return '', code

    logging.debug('get for key [%s]', req['key'])
    if req['no-cache']:
        value = table.find_one({'key': req['key']})
        if value is not None:
            code = 200
            tmp = json.dumps({"status": "Ok", "message": value})
            return tmp.encode("utf-8"), code
        else:
            logging.error('no data in database for key [%s]', req['key'])
            code = 404
            return '', code
    else:
        if req['key'] in cache.keys():
            code = 200
            tmp = json.dumps({"status": "Ok", "message": cache[req['key']]})
            return tmp.encode("utf-8"), code
        else:
            logging.warning('no data in cache for key [%s]', req['key'])
            value = table.find_one({'key': req['key']})
            if value is not None:
                code = 200
                cache[req['key']] = value
                tmp = json.dumps({"status": "Ok", "message": value})
                return tmp.encode("utf-8"), code
            else:
                logging.error('no data in database for key [%s]', req['key'])
                code = 404
                return '', code


if __name__ == '__main__':
    port = 65432
    host = ''
    app.run(port=port, host=host)