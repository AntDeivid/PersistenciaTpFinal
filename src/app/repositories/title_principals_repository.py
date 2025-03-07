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


class TitlePrincipalsRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create(self, title_principals: TitlePrincipals) -> TitlePrincipals:
        try:
            with next(get_db()) as db:
                db.add(title_principals)
                db.commit()
                db.refresh(title_principals)
                self.logger.info(f"TitlePrincipals criado com sucesso! tconst: {title_principals.tconst}")
                return title_principals
        except IntegrityError:
            self.logger.error(f"Erro ao criar TitlePrincipals! tconst: {title_principals.tconst}")
            raise ValueError(f"Erro ao criar TitlePrincipals com tconst: {title_principals.tconst}")

    def get_by_tconst(self, tconst: str) -> Optional[TitlePrincipals]:
        with next(get_db()) as db:
            self.logger.info(f"Buscando TitlePrincipals com tconst {tconst}")
            return db.query(TitlePrincipals).filter(TitlePrincipals.tconst == tconst).first()

    def update(self, tconst: str, title_principals: TitlePrincipals) -> Optional[TitlePrincipals]:
        try:
            with next(get_db()) as db:
                existing_title_principals = db.query(TitlePrincipals).filter(TitlePrincipals.tconst == tconst).first()
                if not existing_title_principals:
                    self.logger.warning(f"TitlePrincipals com tconst {tconst} não encontrado para atualização.")
                    return None

                # Update fields
                existing_title_principals.ordering = title_principals.ordering
                existing_title_principals.nconst = title_principals.nconst
                existing_title_principals.category = title_principals.category
                existing_title_principals.job = title_principals.job
                existing_title_principals.characters = title_principals.characters

                db.commit()
                db.refresh(existing_title_principals)
                self.logger.info(f"TitlePrincipals com tconst {tconst} atualizado com sucesso!")
                return existing_title_principals
        except IntegrityError as e:
            db.rollback()
            self.logger.error(f"Erro ao atualizar TitlePrincipals com tconst {tconst}: {e}")
            raise ValueError(f"Erro ao atualizar TitlePrincipals com tconst: {tconst}")
        
    def delete(self, tconst: str) -> bool:
        with next(get_db()) as db:
            title_principals = db.query(TitlePrincipals).filter(TitlePrincipals.tconst == tconst).first()
            if not title_principals:
                self.logger.warning(f"TitlePrincipals com tconst {tconst} não encontrado para exclusão.")
                return False

            db.delete(title_principals)
            db.commit()
            self.logger.info(f"TitlePrincipals com tconst {tconst} excluído com sucesso!")
            return True
        
    def get_all(self, page: int, limit: int) -> PaginationResultDto:
        with next(get_db()) as db:
            query = db.query(TitlePrincipals)
            total = query.count()
            title_principals = query.offset((page - 1) * limit).limit(limit).all()
            return PaginationResultDto(total=total, items=title_principals)
        