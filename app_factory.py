from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

from telemetry import setup_telemetry

tracer = setup_telemetry("journal-service")
HTTPXClientInstrumentor().instrument()


def app_factory():
    app = FastAPI(default_response_class=ORJSONResponse)
    return app
