import argparse
import leveldb
import ujson as json
from flask import request, g

from flatdb import flatdb_app


JSON = {'Content-Type': 'application/json'}


def ensure_db():
    if 'db' not in g:
        g.db = leveldb.LevelDB(flatdb_app.config['DB'])


def put():
    ensure_db()
    keys = request.args.items(multi=True)
    batch = leveldb.WriteBatch()
    for k, v in keys:
        batch.Put(k, v)
    g.db.Write(batch)
    return '', 201, JSON


def get():
    ensure_db()
    keys = request.args.getlist('key')
    if not keys:
        return '', 204, JSON
    response = {}
    for k in keys:
        try:
            response[k] = g.db.Get(k)
        except KeyError:
            pass
    if not response:
        return '', 404, JSON
    return json.dumps(response), 200, JSON


def getrange():
    ensure_db()
    from_key = request.args.get('from')
    response = {}
    vals = g.db.RangeIter(key_from=from_key)
    for k, v in vals:
        response[k] = v
    if not response:
        return '', 404, JSON
    return json.dumps(response), 200, JSON


def delete():
    ensure_db()
    keys = request.args.getlist('key')
    batch = leveldb.WriteBatch()
    for k in keys:
        batch.Delete(k)
    g.db.Write(batch)
    return '', 200, JSON


def define_urls(app):
    app.add_url_rule('/put', view_func=put, methods=['GET'])
    app.add_url_rule('/get', view_func=get, methods=['GET'])
    app.add_url_rule('/getrange', view_func=getrange, methods=['GET'])
    app.add_url_rule('/delete', view_func=delete, methods=['GET'])


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', default=False)
    parser.add_argument('-p', '--port', type=int, default=7532)
    parser.add_argument('-b', '--database')
    parser.add_argument('-H', '--host', default='127.0.0.1')
    return parser.parse_args()


def configure_app(app, options):
    app.config['DB'] = options.database
    define_urls(app)


def dev_server():
    options = get_options()
    configure_app(flatdb_app, options)
    flatdb_app.run(debug=options.debug, port=options.port, host=options.host)


def run_server():
    options = get_options()
    configure_app(flatdb_app, options)

    from gevent.wsgi import WSGIServer

    server = WSGIServer((options.host, options.port), flatdb_app)
    server.serve_forever()


if __name__ == '__main__':
    run_server()
