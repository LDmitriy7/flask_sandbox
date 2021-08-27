import mongoengine as me
from flask import Flask, redirect, request, url_for

import config

app = Flask(__name__)

me.connect(
    db='my-bots',
    username=config.DB_USERNAME,
    password=config.DB_PASSWORD,
    authentication_source=config.DB_AUTH_SOURCE,
)


class Redirect(me.Document):
    key: str = me.StringField(unique=True)
    src: str = me.StringField()


@app.route('/')
def index():
    return 'Hello, world!'


@app.route('/redirect/<key>')
def redirect_(key: str):
    redirect_doc = Redirect.objects(key=key).first()

    if redirect_doc is None:
        return 'Redirect not found.'

    return redirect(redirect_doc.src)


@app.route('/redirects/add')
def add_redirect():
    required_args = ('key', 'src', 'token')

    try:
        key, src, token = (request.args[i] for i in required_args)
    except:
        route = url_for('add_redirect')
        args = "&".join(f'{a}=.' for a in required_args)
        return f'{route}?{args}'

    if token != config.TOKEN:
        return 'Wrong token.'

    redirect_doc = Redirect.objects(key=key).first()

    if redirect_doc is None:
        Redirect(key=key, src=src).save()
    else:
        redirect_doc.src = src
        redirect_doc.save()

    redirect_url = url_for('redirect_', key=key, _external=True)
    return f'<a href="{redirect_url}" >{redirect_url}</a>'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
