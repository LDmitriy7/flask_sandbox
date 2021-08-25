from aiohttp import web
import ssl
import config

app = web.Application()


async def index(request: web.Request):
    print(request.values())
    return web.Response(text='Hello, world!')


async def check_ip(request: web.Request):
    return web.Response(text=request.remote)


app.router.add_get('/', index)
app.router.add_get('/check_ip', check_ip)


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
