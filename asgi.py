import uvicorn

from billing.app.fastapi import app  # noqa

if __name__ == '__main__':
    uvicorn.run('asgi:app', host='127.0.0.1', port=5000, log_level='debug', reload=True)
