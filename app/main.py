from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from app.db.client import db
from app.routers import auth, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.connect()
    yield
    # Shutdown
    await db.disconnect()
    
app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(user.router)
