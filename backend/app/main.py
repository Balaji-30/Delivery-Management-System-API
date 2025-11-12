from contextlib import asynccontextmanager
from time import perf_counter

from fastapi import FastAPI, Request, Response
from fastapi.routing import APIRoute
from scalar_fastapi import get_scalar_api_reference
from fastapi.middleware.cors import CORSMiddleware

from app.api.core.exceptions import add_exception_handlers
from app.database.session import create_db_tables

from app.api.router import master_router
from app.worker.tasks import add_log

description = """
Delivery Management System for sellers and delivery agents.

Features include:

###Sellers
- Submit shipment requests effortlessly
- Share tracking details with customers

###Delivery Agents
- Auto accept shipments
- Track and update shipment status
- Email and SMS notifications
"""


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_db_tables()
    yield
    print("server ended")

def custom_generate_unique_id(route: APIRoute) -> str:
     return route.name

app = FastAPI(
    title="Shippin",
    description=description,
    docs_url= None,
    version="0.1.0",
    lifespan=lifespan_handler,
    servers=[
        {"url": "http://127.0.0.1:8000", "description": "Local Development Server"}
    ],
    generate_unique_id_function=custom_generate_unique_id,
)

@app.get("/")
async def read_root():
        return {"message": "Welcome to Shippin - Delivery Management System API"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

app.include_router(master_router)

add_exception_handlers(app)


@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    start = perf_counter()
    response: Response = await call_next(request)
    end = perf_counter()
    time_taken = round(end - start, 2)
    add_log.delay(
        f"{request.method} {request.url} - {response.status_code} - {time_taken}s"
    )
    return response


@app.get("/docs", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
