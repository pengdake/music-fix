from app.core.handler import register_exception_handlers
from app.middlewares.logging import register_middleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import router  
import uvicorn
from app.lifespan import lifespan


app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

register_middleware(app)
register_exception_handlers(app)

app.include_router(router, prefix="/api/v1", tags=["v1"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
