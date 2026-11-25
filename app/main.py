from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.kafka_producer import start_producer, stop_producer
from app.api.auth import router as auth_router
from app.core.exceptions import AppError


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Запускаем продюсера
    await start_producer()
    yield
    # Останавливаем при выключении
    await stop_producer()


app = FastAPI(title="Auth Service", lifespan=lifespan)
app.include_router(auth_router)


@app.exception_handler(AppError)
async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
