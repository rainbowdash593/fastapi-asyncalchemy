from dotenv import load_dotenv

load_dotenv()

import uvicorn
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.core.settings import settings
from app.api.v1.router import router

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS] if settings.BACKEND_CORS_ORIGINS else ['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
