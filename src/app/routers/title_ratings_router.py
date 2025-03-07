from typing import Optional, List

from fastapi import APIRouter, HTTPException, status, Query, Path

from src.app.models.title_ratings import TitleRatings
from src.app.dtos.PaginationResultDto import PaginationResultDto
from src.app.repositories.title_ratings_repository import TitleRatingsRepository

title_ratings_router = APIRouter(prefix="/api/ratings", tags=["Ratings"])

title_ratings_repository = TitleRatingsRepository()


@title_ratings_router.post("/", response_model=TitleRatings, status_code=status.HTTP_201_CREATED)
def create_rating(rating: TitleRatings):
    try:
        return title_ratings_repository.create(rating)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@title_ratings_router.get("/{tconst}", response_model=Optional[TitleRatings])
def get_rating_by_tconst(tconst: str = Path(..., title="The ID of the title to get rating for")):
    rating = title_ratings_repository.get_by_tconst(tconst)
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Avaliação não encontrada"
        )
    return rating


@title_ratings_router.put("/{tconst}", response_model=Optional[TitleRatings])
def update_rating(
    tconst: str = Path(..., title="The ID of the title to update rating for"),
    averageRating: float = Query(..., ge=0, le=10, title="New average rating"),
    numVotes: int = Query(..., ge=0, title="New number of votes"),
):
    updated_rating = title_ratings_repository.update(tconst, averageRating, numVotes)
    if not updated_rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Avaliação não encontrada"
        )
    return updated_rating


@title_ratings_router.delete("/{tconst}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(tconst: str = Path(..., title="The ID of the title to delete rating for")):
    deleted = title_ratings_repository.delete(tconst)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Avaliação não encontrada"
        )
    return None


@title_ratings_router.get("/above/", response_model=PaginationResultDto)
def get_ratings_above(
    min_rating: float = Query(..., ge=0, le=10, title="Minimum rating"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    return title_ratings_repository.get_ratings_above(min_rating, page, limit)


@title_ratings_router.get("/by-votes/", response_model=PaginationResultDto)
def get_ratings_by_votes(
    min_votes: int = Query(..., ge=0, title="Minimum number of votes"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    return title_ratings_repository.get_ratings_by_votes(min_votes, page, limit)

@title_ratings_router.get("/top-voted/")
def get_top_n_voted(n: int = Query(10, ge=1, le=100, title="Number of top voted titles to retrieve")):
    return title_ratings_repository.get_top_n_voted(n)

@title_ratings_router.get("/highest-rated/")
def get_highest_rated(n: int = Query(10, ge=1, le=100, title="Number of highest rated titles to retrieve")):
    return title_ratings_repository.get_highest_rated(n)

@title_ratings_router.get("/average-by-title-type/")
def get_average_rating_by_title_type(title_type: str = Query(..., title="Type of the title to average rating")):
    return title_ratings_repository.get_average_rating_by_title_type(title_type)

@title_ratings_router.get("/average-by-director/")
def get_average_rating_by_director(director_name: str = Query(..., title="Name of the director to average rating")):
    return title_ratings_repository.get_average_rating_by_director(director_name)

@title_ratings_router.get("/", response_model=List[TitleRatings])
def get_all_ratings():
    return title_ratings_repository.get_all()