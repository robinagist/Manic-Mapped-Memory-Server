from sanic import response


def teapot():
    pl = "{'manic':'I am a teapot'}"
    return response.json(pl, status=418)