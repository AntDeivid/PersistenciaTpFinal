from typing import Optional, List

from fastapi import APIRouter, HTTPException, status, Path,Query
from src.app.dtos.PaginationResultDto import PaginationResultDto
from src.app.models.title_principals import TitlePrincipals
from src.app.repositories.title_principals_repository import TitlePrincipalsRepository

title_principals_router = APIRouter(prefix="/api/title_principals", tags=["Title Principals"])

title_principals_repository = TitlePrincipalsRepository()


@title_principals_router.post("/", response_model=TitlePrincipals, status_code=status.HTTP_201_CREATED)
def create_title_principals(title_principals: TitlePrincipals):
    try:
        return title_principals_repository.create(title_principals)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

@title_principals_router.get("/{tconst}/{ordering}", response_model=Optional[TitlePrincipals])
def get_title_principals_by_tconst_and_ordering(tconst: str = Path(..., title="The tconst of the title principals to get"), ordering: int = Path(..., title="The ordering of the title principals to get")):
    title_principals = title_principals_repository.get_by_tconst_and_ordering(tconst, ordering)
    if not title_principals:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="TitlePrincipals não encontrado"
        )
    return title_principals


@title_principals_router.put("/{tconst}/{ordering}", response_model=Optional[TitlePrincipals])
def update_title_principals(tconst: str = Path(..., title="The tconst of the title principals to update"), ordering: int = Path(..., title="The ordering of the title principals to update"), title_principals: TitlePrincipals = None):
    updated_title_principals = title_principals_repository.update(tconst, ordering, title_principals)
    if not updated_title_principals:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="TitlePrincipals não encontrado"
        )
    return updated_title_principals


@title_principals_router.delete("/{tconst}/{ordering}", status_code=status.HTTP_204_NO_CONTENT)
def delete_title_principals(tconst: str, ordering: int):
    deleted = title_principals_repository.delete(tconst, ordering)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="TitlePrincipals não encontrado"
        )
    return None

@title_principals_router.get("/", response_model=PaginationResultDto)
def get_all_title_principals(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    return title_principals_repository.get_all(page, limit)
