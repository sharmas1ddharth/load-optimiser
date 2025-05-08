from fastapi import FastAPI
from api.routing.binpacking_router.binpacking_router import binpacking_router

app = FastAPI(
    title="Load Optimiser", description="Load Optimiser Server API", version="1.0.0"
)

app.include_router(binpacking_router)