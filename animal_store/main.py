from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from animal_store import config
from animal_store.deps import db_manager
from animal_store.routers import animals, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_manager:
        yield


app = FastAPI(title="Animal Store", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(users.router)
app.include_router(animals.router)


if __name__=="__main__":
    uvicorn.run(app, host=config.HOST, port=config.PORT)
