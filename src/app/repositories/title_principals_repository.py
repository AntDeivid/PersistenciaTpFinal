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
        # chave composta: (tconst, ordering)
        tconst = title_principals.tconst
        ordering = title_principals.ordering
        with next(get_db()) as db:
            existing_title_principals = db.query(TitlePrincipals).filter(TitlePrincipals.tconst == tconst, TitlePrincipals.ordering == ordering).first()
            if existing_title_principals:
                self.logger.warning(f"TitlePrincipals com tconst {tconst} e ordering {ordering} já existe.")
                raise ValueError(f"TitlePrincipals com tconst {tconst} e ordering {ordering} já existe.")

            try:
                db.add(title_principals)
                db.commit()
                db.refresh(title_principals)
                self.logger.info(f"TitlePrincipals criado com sucesso! tconst: {title_principals.tconst}")
                return title_principals
            except IntegrityError:
                self.logger.error(f"Erro ao criar TitlePrincipals! tconst: {title_principals.tconst}")
                raise ValueError(f"Erro ao criar TitlePrincipals com tconst: {title_principals.tconst}")

    def get_by_tconst_and_ordering(self, tconst: str, ordering: int) -> Optional[TitlePrincipals]:
        with next(get_db()) as db:
            self.logger.info(f"Buscando TitlePrincipals com tconst {tconst} e ordering {ordering}")
            return db.query(TitlePrincipals).filter(TitlePrincipals.tconst == tconst, TitlePrincipals.ordering == ordering).first()

    def update(self, tconst: str, ordering: int, title_principals: TitlePrincipals) -> Optional[TitlePrincipals]:
        with next(get_db()) as db:
            existing_title_principals = db.query(TitlePrincipals).filter(TitlePrincipals.tconst == tconst, TitlePrincipals.ordering == ordering).first()
            if not existing_title_principals:
                self.logger.warning(f"TitlePrincipals com tconst {tconst} e ordering {ordering} não encontrado para atualização.")
                return None

            # Update fields
            existing_title_principals.nconst = title_principals.nconst
            existing_title_principals.category = title_principals.category
            existing_title_principals.job = title_principals.job
            existing_title_principals.characters = title_principals.characters

            db.commit()
            db.refresh(existing_title_principals)
            self.logger.info(f"TitlePrincipals com tconst {tconst} e ordering {ordering} atualizado com sucesso!")
            return existing_title_principals
        
    def delete(self, tconst: str, ordering: int) -> bool:
        with next(get_db()) as db:
            title_principals = db.query(TitlePrincipals).filter(TitlePrincipals.tconst == tconst, TitlePrincipals.ordering == ordering).first()
            if not title_principals:
                self.logger.warning(f"TitlePrincipals com tconst {tconst} e ordering {ordering} não encontrado para deleção.")
                return False
            db.delete(title_principals)
            db.commit()
            self.logger.info(f"TitlePrincipals com tconst {tconst} e ordering {ordering} deletado com sucesso!")
            return True
        
    def get_all(self, page: int, limit: int) -> PaginationResultDto:
        with next(get_db()) as db:
            query = db.query(TitlePrincipals)
            total = query.count()
            number_of_pages = (total + limit - 1) // limit
            data = query.offset((page - 1) * limit).limit(limit).all()

            return PaginationResultDto(
                page=page,
                limit=limit,
                total_items=total,
                number_of_pages=number_of_pages,
                data=data
            )    