from app.core.handler import register_exception_handlers
from app.core.middleware import register_middleware
from fastapi import FastAPI
from app.api.routers import music
import uvicorn
from app.core.lifespan import lifespan


app = FastAPI(lifespan=lifespan)

register_middleware(app)
register_exception_handlers(app)

app.include_router(music.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
