import asyncio
import functools
import os

from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import SpanProcessor, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def sync_trace_span_function(tracer: trace.Tracer):
    def decorator_trace_span_function(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with tracer.start_as_current_span(func.__name__):
                return func(*args, **kwargs)

        return wrapper

    return decorator_trace_span_function


def trace_span_function(tracer: trace.Tracer):
    def decorator_trace_span_function(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if not asyncio.iscoroutinefunction(func):
                with tracer.start_as_current_span(func.__name__):
                    return func(*args, **kwargs)
            else:
                with tracer.start_as_current_span(func.__name__):
                    return await func(*args, **kwargs)

        return wrapper

    return decorator_trace_span_function


def setup_telemetry(service_name: str) -> trace.Tracer:
    """
    Sets up telemetry to be used on the app. This sets the Tracer Provider
    with the service name passed to this function. This allows to see the service name
    on the app
    This also gets a trace provider (Jaeger for now)
    Returns a trace.Tracer object that can be used in two ways:
    1 - With a decorator (defined above)
    ```
    tracer = setup_telemetry("sample")
    @trace_span_function(tracer=tracer)
    def my_func(*args):
        ...
    ```
    2 - As a context manager
    ```
    tracer = setup_telemetry("sample")
    async def my_func(*args):
        ...
    async def current_function(...):
        with tracer.start_as_current_span("span name"):
            result = await my_func(...)
    ```
    """
    trace.set_tracer_provider(
        TracerProvider(resource=Resource.create({SERVICE_NAME: service_name}))
    )
    tracer = trace.get_tracer(__name__)
    trace.get_tracer_provider().add_span_processor(get_span_processor())
    return tracer


def get_span_processor():
    trace_exporter = os.environ.get("ENABLE_TRACE_EXPORTER", "")
    if trace_exporter == "jaeger":
        jaeger_exporter = JaegerExporter(
            # configure agent
            agent_host_name="jaeger",
            agent_port=6831,
            udp_split_oversized_batches=True,
        )
        return BatchSpanProcessor(jaeger_exporter)
    elif trace_exporter == "cloud-trace":
        exporter = CloudTraceSpanExporter()
        return BatchSpanProcessor(exporter)
    return SpanProcessor()
