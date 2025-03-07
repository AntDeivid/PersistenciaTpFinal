from typing import Optional

from fastapi import APIRouter, HTTPException, status, Path,Query
from src.app.dtos.PaginationResultDto import PaginationResultDto
from src.app.models.title_crew import TitleCrew
from src.app.repositories.title_crew_repository import TitleCrewRepository

title_crew_router = APIRouter(prefix="/api/title_crew", tags=["Title Crew"])

title_crew_repository = TitleCrewRepository()


@title_crew_router.post("/", response_model=TitleCrew, status_code=status.HTTP_201_CREATED)
def create_title_crew(title_crew: TitleCrew):
    try:
        return title_crew_repository.create(title_crew)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@title_crew_router.get("/{tconst}", response_model=Optional[TitleCrew])
def get_title_crew_by_tconst(tconst: str = Path(..., title="The tconst of the title crew to get")):
    title_crew = title_crew_repository.get_by_tconst(tconst)
    if not title_crew:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="TitleCrew não encontrado"
        )
    return title_crew


@title_crew_router.put("/{tconst}", response_model=Optional[TitleCrew])
def update_title_crew(tconst: str = Path(..., title="The tconst of the title crew to update"), title_crew: TitleCrew = None):
    updated_title_crew = title_crew_repository.update(tconst, title_crew)
    if not updated_title_crew:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="TitleCrew não encontrado"
        )
    return updated_title_crew


@title_crew_router.delete("/{tconst}", status_code=status.HTTP_204_NO_CONTENT)
def delete_title_crew(tconst: str):
    deleted = title_crew_repository.delete(tconst)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="TitleCrew não encontrado"
        )
    return None

@title_crew_router.get("/", response_model=PaginationResultDto)
def get_all_title_crew(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    return title_crew_repository.get_all(page, limit)