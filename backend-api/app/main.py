# FastAPI Import
from fastapi import FastAPI

# Own Import
import routers

app = FastAPI()

# Include API router
app.include_router(routers.router)

