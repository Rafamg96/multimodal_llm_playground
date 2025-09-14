from fastapi import APIRouter
from fastapi.responses import JSONResponse

namespace="status"
status_router = APIRouter(prefix=f"/{namespace}")

@status_router.get("",tags=[namespace])
async def get_status():
    return JSONResponse("API works!!")
