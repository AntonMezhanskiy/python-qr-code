# -*- coding: utf-8 -*-

import bottle
import os
import json

from bottle import view, request, response, template, redirect
import qrcode

bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')

# myapp = bottle.default_app()
myapp = bottle.Bottle()

@myapp.route('/static/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root=STATIC_ROOT)
    

@myapp.route('/')
@myapp.route('/home')
def home():
  return template('index.tpl')



@myapp.route('/add.json', method='POST')
def addjson():
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(request.json['text'])
    qr.make(fit=True)
    x = qr.make_image()

    qr_file = os.path.join(PROJECT_ROOT + "/static/images/", str(request.json['len']) + ".jpg")
    img_file = open(qr_file, 'wb')
    x.save(img_file, 'JPEG')
    img_file.close()

    return json.dumps({'ok': True})




@myapp.error(403)
def mistake403(code):
    return 'There is a mistake in your url!'


@myapp.error(405)
def mistake405(code):
    return 'There is a mistake in your url!'


@myapp.error(404)
def mistake404(code):
    return template('404.tpl')
    # return 'Sorry, this page does not exist!'


if __name__ == '__main__':
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')
    HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '9999'))
    except ValueError:
        PORT = 9999

    myapp.run(reloader=True, host=HOST, port=PORT)
