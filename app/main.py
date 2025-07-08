from fastapi import FastAPI, status
from fastapi.concurrency import asynccontextmanager
from app.db.client import db
from app.routers import auth, user, plan, feature, subscription, order
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",  # React frontend
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.connect()
    yield
    # Shutdown
    await db.disconnect()


app = FastAPI(lifespan=lifespan)
@app.get("/", status_code=status.HTTP_200_OK)
async def hello_world():
    return {"msg": "Hello World"}
    
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(plan.router)
app.include_router(feature.router)
app.include_router(subscription.router)
app.include_router(order.router)
