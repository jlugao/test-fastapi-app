from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import async_get_settings, get_settings
from telemetry import get_span_processor

settings = get_settings()
engine = create_async_engine(settings.POSTGRES_URL, future=True, echo=True)
new_tracer = TracerProvider(resource=Resource.create({SERVICE_NAME: "db"}))
new_tracer.add_span_processor(get_span_processor())
SQLAlchemyInstrumentor().instrument(
    engine=engine.sync_engine, tracer_provider=new_tracer
)


async def get_db():
    """Create a session object to be used in async Postgres calls."""

    session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False, future=True
    )
    async with session() as db_session:
        yield db_session
