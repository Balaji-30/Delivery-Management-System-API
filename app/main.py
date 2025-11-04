from contextlib import asynccontextmanager
from time import perf_counter

from fastapi import FastAPI, Request, Response
from scalar_fastapi import get_scalar_api_reference
from fastapi.middleware.cors import CORSMiddleware

from app.api.core.exceptions import add_exception_handlers
from app.database.session import create_db_tables

from app.api.router import master_router
from app.worker.tasks import add_log


@asynccontextmanager
async def lifespan_handler(app:FastAPI):
        await create_db_tables()
        yield
        print("server ended")

app=FastAPI(title="Shippin",lifespan=lifespan_handler,servers=[{"url": "http://127.0.0.1:8000", "description": "Local Development Server"}])

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
)

app.include_router(master_router)

add_exception_handlers(app)

@app.middleware("http")
async def custom_middleware(request: Request, call_next):
        start = perf_counter()
        response: Response = await call_next(request)
        end = perf_counter()
        time_taken = round(end - start,2)
        add_log.delay(f"{request.method} {request.url} - {response.status_code} - {time_taken}s")
        return response


@app.get("/scalar",include_in_schema=False)
def get_scalar_docs():
        return get_scalar_api_reference(
                openapi_url=app.openapi_url,
                title="Scalar API"

        )  