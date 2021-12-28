from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


def app_factory():
    app = FastAPI(default_response_class=ORJSONResponse)
    return app
