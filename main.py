from fastapi import FastAPI
from app.database import engine, Base
from app.notifications import notifications
from app.user import user
from app.sender import tasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

app = FastAPI(
    openapi_url="/notifications/openapi.json",
    docs_url="/notifications/docs",
    redoc_url="/notifications/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notifications.router)
app.include_router(user.router)

add_pagination(app)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
