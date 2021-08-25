from aiohttp import web
import ssl
import config
from datetime import datetime

app = web.Application()

index_text = """\
<html>
<head>
    <title>My site</title>
    <meta name="google-site-verification" content="iDBCzMVJ5DlWMqAou4OBQAlByIHbrwFBq-VNUqUvxmE" />
</head>
<body>
    <h1>Hello, world!</h1>
</body>
</html>
"""


async def index(request: web.Request):
    print(request.values())
    return web.Response(text=index_text, content_type='text/html')


async def check_ip(request: web.Request):
    return web.Response(text=request.remote)


async def timestamp(_request: web.Request):
    return web.Response(text=str(datetime.now().timestamp()))


async def date(request: web.Request):
    if timestamp := request.query.get('timestamp'):
        dt = datetime.fromtimestamp(float(timestamp))
    else:
        dt = datetime.now()

    return web.Response(text=str(dt))


app.router.add_get('/', index)
app.router.add_get('/check-ip', check_ip)
app.router.add_get('/timestamp', timestamp)
app.router.add_get('/date', date)


def main():
    try:
        ssl_context = ssl.SSLContext()
        ssl_context.load_cert_chain(config.SSL_CERT_FILE, config.SSL_KEY_FILE)
        port = 443
    except (OSError, TypeError):
        ssl_context = None
        port = 80

    web.run_app(app, ssl_context=ssl_context, port=port)


if __name__ == '__main__':
    main()
