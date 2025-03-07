from fastapi.routing import APIRouter

from src.app.routers.title_basics_router import title_basics_router
from src.app.routers.title_crew_router import title_crew_router
from src.app.routers.title_principals_router import title_principals_router
from src.app.routers.title_ratings_router import title_ratings_router

router = APIRouter()

router.include_router(title_basics_router)
router.include_router(title_crew_router)
router.include_router(title_principals_router)
router.include_router(title_ratings_router)
