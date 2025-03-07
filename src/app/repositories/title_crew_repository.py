import logging
from typing import Optional,List
from src.app.dtos.PaginationResultDto import PaginationResultDto
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from src.app.core.db.database import get_db
#models
from src.app.models.title_crew import TitleCrew
from src.app.models.title_basics import TitleBasics
from src.app.models.title_ratings import TitleRatings
from src.app.models.title_principals import TitlePrincipals
from src.app.models.name_basics import NameBasics


class TitleCrewRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create(self, title_crew: TitleCrew) -> TitleCrew:
        try:
            with next(get_db()) as db:
                db.add(title_crew)
                db.commit()
                db.refresh(title_crew)
                self.logger.info(f"TitleCrew criado com sucesso! tconst: {title_crew.tconst}")
                return title_crew
        except IntegrityError:
            self.logger.error(f"Erro ao criar TitleCrew! tconst: {title_crew.tconst}")
            raise ValueError(f"Erro ao criar TitleCrew com tconst: {title_crew.tconst}")

    def get_by_tconst(self, tconst: str) -> Optional[TitleCrew]:
        with next(get_db()) as db:
            self.logger.info(f"Buscando TitleCrew com tconst {tconst}")
            return db.query(TitleCrew).filter(TitleCrew.tconst == tconst).first()

    def update(self, tconst: str, title_crew: TitleCrew) -> Optional[TitleCrew]:
        try:
            with next(get_db()) as db:
                existing_title_crew = db.query(TitleCrew).filter(TitleCrew.tconst == tconst).first()
                if not existing_title_crew:
                    self.logger.warning(f"TitleCrew com tconst {tconst} não encontrado para atualização.")
                    return None

                # Update fields
                existing_title_crew.directors = title_crew.directors
                existing_title_crew.writers = title_crew.writers

                db.commit()
                db.refresh(existing_title_crew)
                self.logger.info(f"TitleCrew com tconst {tconst} atualizado com sucesso!")
                return existing_title_crew
        except IntegrityError as e:
            db.rollback()
            self.logger.error(f"Erro ao atualizar TitleCrew com tconst {tconst}: {e}")
            raise ValueError(f"Erro ao atualizar TitleCrew com tconst: {tconst}")

    def delete(self, tconst: str) -> bool:
        with next(get_db()) as db:
            title_crew = db.query(TitleCrew).filter(TitleCrew.tconst == tconst).first()
            if not title_crew:
                self.logger.warning(f"TitleCrew com tconst {tconst} não encontrado para deleção.")
                return False
            db.delete(title_crew)
            db.commit()
            self.logger.info(f"TitleCrew com tconst {tconst} deletado")
            return True
    
    def get_all(self, page: int = 1, limit: int = 10) -> PaginationResultDto:
        with next(get_db()) as db:
            query = db.query(TitleCrew)
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
            