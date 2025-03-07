from typing import Optional,List
from fastapi import APIRouter, HTTPException, status, Query, Path
from src.app.dtos.TitleBasicWithCastDto import TitleBasicsWithCast
from src.app.models.title_basics import TitleBasics
from src.app.dtos.PaginationResultDto import PaginationResultDto
from src.app.repositories.title_basics_repository import TitleBasicsRepository

title_basics_router = APIRouter(prefix="/api/titles", tags=["Titles"])

title_basics_repository = TitleBasicsRepository()


@title_basics_router.post("/", response_model=TitleBasics, status_code=status.HTTP_201_CREATED)
def create_title(title: TitleBasics):
    try:
        return title_basics_repository.create(title)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@title_basics_router.get("/", response_model=PaginationResultDto)
def get_titles(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    return title_basics_repository.get_all(page, limit)


@title_basics_router.get("/search", response_model=PaginationResultDto)
def search_titles(
    title: str = Query(..., title="The title to search for"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    return title_basics_repository.search_by_title(title, page, limit)


@title_basics_router.get("/by-genre/")
def get_titles_by_genre(
    genre: str = Query(..., title="Genre to filter by"),
    min_rating: Optional[float] = Query(None, ge=0, le=10),
):
    return title_basics_repository.get_by_genre(genre, min_rating)


@title_basics_router.get("/top-rated/")
def get_top_rated_titles(limit: int = Query(10, ge=1, le=100)):
    return title_basics_repository.get_top_rated_titles(limit)


@title_basics_router.get("/{tconst}", response_model=Optional[TitleBasics])
def get_title_by_id(tconst: str = Path(..., title="The ID of the title to get")):
    title = title_basics_repository.get_by_tconst(tconst)
    if not title:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Título não encontrado"
        )
    return title


@title_basics_router.get("/crew-cast/{tconst}", response_model=Optional[TitleBasics])
def get_title_with_crew_and_cast(tconst: str = Path(..., title="Title ID")):
    title = title_basics_repository.get_titles_with_crew_and_cast(tconst)
    if not title:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Título não encontrado"
        )
    return title


@title_basics_router.get("/by-director/{director_name}")
def get_titles_by_director(director_name: str = Path(..., title="The director's name")):
    return title_basics_repository.get_titles_by_director(director_name)


@title_basics_router.delete("/{tconst}", status_code=status.HTTP_204_NO_CONTENT)
def delete_title(tconst: str):
    deleted = title_basics_repository.delete(tconst)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Título não encontrado"
        )
    return None

@title_basics_router.get(
    "/by-genre-rating-cast/",
    response_model=List[TitleBasicsWithCast]
)
def get_titles_by_genre_rating_cast(
    genre: str = Query("Reality_TV", title="Genre to filter by"),
    min_rating: float = Query(..., title="Minimum rating"),
):
    titles = title_basics_repository.get_titles_by_genre_and_rating_with_cast(genre, min_rating)
    return titles