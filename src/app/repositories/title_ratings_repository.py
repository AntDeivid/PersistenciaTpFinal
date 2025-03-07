import logging
from typing import Optional, List

from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

from src.app.core.db.database import get_db
from src.app.dtos.PaginationResultDto import PaginationResultDto
from src.app.models.title_basics import TitleBasics
from src.app.models.title_crew import TitleCrew
from src.app.models.title_ratings import TitleRatings


class TitleRatingsRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create(self, rating: TitleRatings) -> TitleRatings:
        try:
            with next(get_db()) as db:
                db.add(rating)
                db.commit()
                db.refresh(rating)
                self.logger.info(f"Avaliação do título {rating.tconst} criada com sucesso!")
                return rating
        except IntegrityError:
            self.logger.error(f"Erro ao criar avaliação para o título {rating.tconst}!")
            raise ValueError(f"Erro ao criar avaliação para o título {rating.tconst}!")

    def get_by_tconst(self, tconst: str) -> Optional[TitleRatings]:
        with next(get_db()) as db:
            self.logger.info(f"Buscando avaliação do título com tconst {tconst}")
            return db.query(TitleRatings).filter(TitleRatings.tconst == tconst).first()

    def update(self, tconst: str, averageRating: float, numVotes: int) -> Optional[TitleRatings]:
        with next(get_db()) as db:
            rating = db.query(TitleRatings).filter(TitleRatings.tconst == tconst).first()
            if rating:
                rating.averageRating = averageRating
                rating.numVotes = numVotes
                db.commit()
                db.refresh(rating)
                self.logger.info(f"Avaliação do título {tconst} atualizada com sucesso!")
                return rating
            else:
                self.logger.warning(f"Avaliação do título {tconst} não encontrada para atualização.")
                return None
            
    def get_all(self) -> List[TitleRatings]:
        with next(get_db()) as db:
            self.logger.info("Buscando todas as avaliações de títulos")
            return db.query(TitleRatings).all()

    def delete(self, tconst: str) -> bool:
        with next(get_db()) as db:
            rating = db.query(TitleRatings).filter(TitleRatings.tconst == tconst).first()
            if rating:
                db.delete(rating)
                db.commit()
                self.logger.info(f"Avaliação do título {tconst} deletada com sucesso!")
                return True
            else:
                self.logger.warning(f"Avaliação do título {tconst} não encontrada para exclusão.")
                return False

    def get_ratings_above(self, min_rating: float, page: int = 1, limit: int = 10) -> PaginationResultDto:
        with next(get_db()) as db:
            query = db.query(TitleRatings).filter(TitleRatings.averageRating >= min_rating)
            total_items = query.count()
            number_of_pages = (total_items + limit - 1) // limit
            data = query.offset((page - 1) * limit).limit(limit).all()

            self.logger.info(f"Buscando avaliações acima de {min_rating}, página {page}, limite {limit}.")

            return PaginationResultDto(
                page=page,
                limit=limit,
                total_items=total_items,
                number_of_pages=number_of_pages,
                data=data
            )

    def get_ratings_by_votes(self, min_votes: int, page: int = 1, limit: int = 10) -> PaginationResultDto:
         with next(get_db()) as db:
            query = db.query(TitleRatings).filter(TitleRatings.numVotes >= min_votes)
            total_items = query.count()
            number_of_pages = (total_items + limit - 1) // limit
            data = query.offset((page - 1) * limit).limit(limit).all()

            self.logger.info(f"Buscando avaliações com no mínimo {min_votes} votos, página {page}, limite {limit}.")

            return PaginationResultDto(
                page=page,
                limit=limit,
                total_items=total_items,
                number_of_pages=number_of_pages,
                data=data
            )

    def get_top_n_voted(self, n: int = 10) -> List[TitleRatings]:
        with next(get_db()) as db:
            self.logger.info(f"Buscando os {n} títulos mais votados")
            return (
                db.query(TitleRatings)
                .order_by(TitleRatings.numVotes.desc())
                .limit(n)
                .all()
            )

    def get_highest_rated(self, n: int = 10) -> List[TitleRatings]:
        with next(get_db()) as db:
            self.logger.info(f"Buscando os {n} títulos com melhor avaliação")
            return (
                db.query(TitleRatings)
                .order_by(TitleRatings.averageRating.desc())
                .limit(n)
                .all()
            )
            
    def get_average_rating_by_title_type(self, title_type: str) -> List[TitleRatings]:
        with next(get_db()) as db:
            self.logger.info(f"Buscando avaliação média dos títulos do tipo {title_type}")
            return db.query(TitleRatings).join(TitleRatings.title).filter(TitleBasics.titleType == title_type).all()  
        
    def get_average_rating_by_director (self, director_name: str) -> List[TitleRatings]:
        with next(get_db()) as db:
            self.logger.info(f"Buscando avaliação média dos títulos dirigidos por {director_name}")
            return db.query(TitleRatings).join(TitleRatings.title).join(TitleBasics.crew).filter(TitleCrew.directors == director_name).all()
          
        
    