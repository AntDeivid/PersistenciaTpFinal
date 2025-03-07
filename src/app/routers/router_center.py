from fastapi.routing import APIRouter

from src.app.routers.title_basics_router import title_basics_router
from src.app.routers.title_crew_router import title_crew_router
router = APIRouter()

router.include_router(title_basics_router)
router.include_router(title_crew_router)