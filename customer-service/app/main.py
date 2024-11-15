from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.customers import customers
from app.api.db import metadata, database, engine, initialize_database, cleanup
from app.api.middleware import LoggingMiddleware
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code: connect to the database
    await initialize_database()
    yield
    # Shutdown code: disconnect from the database
    await cleanup()


app = FastAPI(
    openapi_url="/api/v1/customers/openapi.json",
    docs_url="/api/v1/customers/docs",
    lifespan=lifespan,  # Use lifespan event handler
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(LoggingMiddleware)

app.include_router(customers, prefix="/api/v1/customers", tags=["customers"])
