from loguru import logger
from fastapi import Request, Response, FastAPI
import uuid
import time


def register_middleware(app: FastAPI):

    @app.middleware("http")
    async def log_middleware(request: Request, call_next):
        trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
        request.state.trace_id = trace_id
        start_time = time.time()
        with logger.contextualize(trace_id=trace_id, request_url=str(request.url), method=request.method):
            logger.info(f"Incoming request: {request.method} {request.url}")
            response = await call_next(request)
            duration = time.time() - start_time
            logger.info(f"Completed request: {request.method} {request.url} - Status: {response.status_code} - Duration: {duration:.2f}s")
            response.headers["X-Trace-ID"] = trace_id
            return response
