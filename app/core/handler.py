
from app.schemas.common import ResponseModel
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from loguru import logger
from fastapi.exceptions import RequestValidationError, HTTPException

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        trace_id = getattr(request.state, "trace_id", "N/A")
        logger.exception(f"Unhandled exception: {exc}")
        response = JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "message": "Internal Server Error",
                "data": None
            }
        )
        response.headers["X-Trace-Id"] = trace_id
        return response

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"Validation error: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={
                "code": 422,
                "message": "Validation Error",
                "data": {"errors": exc.errors()}
            }
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.error(f"HTTP error: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "message": exc.detail,
                "data": None
            }
        )   

