import logging
from typing import Optional, List
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

from src.app.core.db.database import get_db
from src.app.dtos.PaginationResultDto import PaginationResultDto
from src.app.models.title_basics import TitleBasics
from src.app.models.title_ratings import TitleRatings
from src.app.models.title_crew import TitleCrew
from src.app.models.title_principals import TitlePrincipals
from src.app.models.name_basics import NameBasics


class TitleBasicsRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create(self, title: TitleBasics) -> TitleBasics:
        try:
            with next(get_db()) as db:
                db.add(title)
                db.commit()
                db.refresh(title)
                self.logger.info("Título criado com sucesso!")
                return title
        except IntegrityError:
            self.logger.error("Erro ao criar título!")
            raise ValueError("Erro ao criar título!")

    def get_by_tconst(self, tconst: str) -> Optional[TitleBasics]:
        with next(get_db()) as db:
            self.logger.info(f"Buscando título com tconst {tconst}")
            return db.query(TitleBasics).filter(TitleBasics.tconst == tconst).first()

    def get_all(self, page: int = 1, limit: int = 10) -> PaginationResultDto:
        with next(get_db()) as db:
            query = db.query(TitleBasics)
            total_items = query.count()
            number_of_pages = (total_items + limit - 1) // limit
            data = query.offset((page - 1) * limit).limit(limit).all()

            return PaginationResultDto(
                page=page,
                limit=limit,
                total_items=total_items,
                number_of_pages=number_of_pages,
                data=data
            )

    def search_by_title(self, title: str, page: int = 1, limit: int = 10) -> PaginationResultDto:
        with next(get_db()) as db:
            query = db.query(TitleBasics).filter(TitleBasics.primaryTitle.ilike(f"%{title}%"))
            total_items = query.count()
            number_of_pages = (total_items + limit - 1) // limit
            data = query.offset((page - 1) * limit).limit(limit).all()

            return PaginationResultDto(
                page=page,
                limit=limit,
                total_items=total_items,
                number_of_pages=number_of_pages,
                data=data
            )

    def get_by_genre(self, genre: str, min_rating: Optional[float] = None) -> List[TitleBasics]:
        with next(get_db()) as db:
            query = db.query(TitleBasics).filter(TitleBasics.genres.ilike(f"%{genre}%"))
            if min_rating:
                query = query.join(TitleRatings).filter(TitleRatings.averageRating >= min_rating)
            self.logger.info(f"Buscando títulos do gênero {genre} com avaliação mínima {min_rating}")
            return query.options(joinedload(TitleBasics.rating)).all()

    def get_top_rated_titles(self, limit: int = 10) -> List[TitleBasics]:
        with next(get_db()) as db:
            self.logger.info("Buscando os títulos mais bem avaliados")
            return (
                db.query(TitleBasics)
                .join(TitleRatings)
                .order_by(TitleRatings.averageRating.desc())
                .limit(limit)
                .all()
            )

    def get_titles_with_crew_and_cast(self, tconst: str) -> Optional[TitleBasics]:
        with next(get_db()) as db:
            self.logger.info(f"Buscando título {tconst} com informações de equipe e elenco")
            return (
                db.query(TitleBasics)
                .filter(TitleBasics.tconst == tconst)
                .options(joinedload(TitleBasics.crew), joinedload(TitleBasics.principals).joinedload(TitlePrincipals.name))
                .first()
            )

    def get_titles_by_director(self, director_name: str) -> List[TitleBasics]:
        with next(get_db()) as db:
            self.logger.info(f"Buscando títulos dirigidos por {director_name}")
            return (
                db.query(TitleBasics)
                .join(TitleCrew)
                .join(NameBasics, TitleCrew.directors.contains(NameBasics.nconst))
                .filter(NameBasics.primaryName.ilike(f"%{director_name}%"))
                .all()
            )

    def delete(self, tconst: str) -> bool:
        with next(get_db()) as db:
            title = db.query(TitleBasics).filter(TitleBasics.tconst == tconst).first()
            if not title:
                return False
            db.delete(title)
            db.commit()
            self.logger.info(f"Título {tconst} deletado")
            return True

    
    def get_titles_by_genre_and_rating_with_cast(self,
        genre: str, min_rating: float
    ) -> List[TitleBasics]:
        with next(get_db()) as db:
            query = (
                db.query(TitleBasics)
                .join(TitleRatings, TitleBasics.tconst == TitleRatings.tconst)
                .join(TitlePrincipals, TitleBasics.tconst == TitlePrincipals.tconst)
                .join(NameBasics, TitlePrincipals.nconst == NameBasics.nconst)
                .filter(TitleBasics.genres.ilike(f"%{genre}%"))
                .filter(TitleRatings.averageRating >= min_rating)
                .options(
                    joinedload(TitleBasics.rating),  
                    joinedload(TitleBasics.principals).joinedload(
                        TitlePrincipals.name
                    ),  
                )
            )
            
            titles = query.all()
            return titles