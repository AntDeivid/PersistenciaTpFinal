from typing import Optional,List
from fastapi import APIRouter, HTTPException, status, Query, Path
from src.app.dtos.TitleBasicWithCastDto import TitleBasicsWithCast
from src.app.models.title_basics import TitleBasics
from src.app.dtos.PaginationResultDto import PaginationResultDto
from src.app.repositories.title_basics_repository import TitleBasicsRepository
from src.app.repositories.name_basics_repository import NameBasicsRepository
from src.app.models.name_basics import NameBasics

name_basics_router = APIRouter(prefix="/name-basics", tags=["Name Basics"])

name_basics_repository = NameBasicsRepository()

@name_basics_router.post("/", response_model=TitleBasics, status_code=status.HTTP_201_CREATED)
def create_name(name: NameBasics):
    try:
        return name_basics_repository.create(name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@name_basics_router.get("/{nconst}", response_model=Optional[NameBasics])
def get_name_by_id(nconst: str = Path(..., title="The ID of the name to get")):
    name = name_basics_repository.get_by_nconst(nconst)
    if not name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nome não encontrado"
        )
    return name
    
@name_basics_router.get("/", response_model=PaginationResultDto)
def get_names(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    return name_basics_repository.get_all(page, limit)

@name_basics_router.get("/search", response_model=PaginationResultDto)
def search_names(
    name: str = Query(..., title="The name to search for"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    return name_basics_repository.search_by_name(name, page, limit)


@name_basics_router.get("/{nconst}/titles", response_model=List[TitleBasicsWithCast])
def get_known_for_titles(nconst: str = Path(..., title="The ID of the name to get")):
    titles = name_basics_repository.get_known_for_titles(nconst)
    if not titles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Títulos não encontrados"
        )
    return titles

@name_basics_router.get("/{nconst}/titles/{tconst}", response_model=Optional[TitleBasicsWithCast])
def get_title_by_id(nconst: str = Path(..., title="The ID of the name to get"), tconst: str = Path(..., title="The ID of the title to get")):
    title = name_basics_repository.get_title_by_id(nconst, tconst)
    if not title:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Título não encontrado"
        )
    return title


# restante:  get_professions
@name_basics_router.get("/{nconst}/professions", response_model=List[str])
def get_professions(nconst: str = Path(..., title="The ID of the name to get")):
    professions = name_basics_repository.get_professions(nconst)
    if not professions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profissões não encontradas"
        )
    return professions