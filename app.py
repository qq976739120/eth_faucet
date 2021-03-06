# -*- coding: utf8 -*-
from flask import Flask
from gevent.pywsgi import WSGIServer
from views import faucet, eth_donate_address, usdt_donate_address
from flask_cors import CORS
from flask_apscheduler import APScheduler

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.debug = True

app.register_blueprint(faucet, url_prefix='')
app.debug = True
http_server = WSGIServer(("0.0.0.0", 5000), app)


class Config(object):
    JOBS = [
        {
            'id': 'job',
            'func': '__main__:clean',
            'args': None,
            'trigger': 'interval',
            # "seconds":20,
            'hours': 6,
            # "minutes":5
        }
    ]


app.config.from_object(Config())


def clean():
    eth_donate_address.clear()
    usdt_donate_address.clear()


if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    http_server.serve_forever()
