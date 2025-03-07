import logging
from src.app.models.name_basics import NameBasics
from typing import Optional, List
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from src.app.core.db.database import get_db
from src.app.dtos.PaginationResultDto import PaginationResultDto


class NameBasicsRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create(self, name: NameBasics) -> NameBasics:
        try:
            with next(get_db()) as db:
                db.add(name)
                db.commit()
                db.refresh(name)
                self.logger.info("Nome criado com sucesso!")
                return name
        except IntegrityError:
            self.logger.error("Erro ao criar nome!")
            raise ValueError("Erro ao criar nome!")
    
    def get_by_nconst(self, nconst: str) -> Optional[NameBasics]:
        with next(get_db()) as db:
            self.logger.info(f"Buscando nome com nconst {nconst}")
            return db.query(NameBasics).filter(NameBasics.nconst == nconst).first()
    
    def get_all(self, page: int = 1, limit: int = 10) -> PaginationResultDto:
        with next(get_db()) as db:
            query = db.query(NameBasics)
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
    
    def search_by_name(self, name: str, page: int = 1, limit: int = 10) -> PaginationResultDto:
        with next(get_db()) as db:
            query = db.query(NameBasics).filter(NameBasics.primaryName.ilike(f"%{name}%"))
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
    
    def get_known_for_titles(self, nconst: str) -> List[str]:
        with next(get_db()) as db:
            self.logger.info(f"Buscando títulos conhecidos para nconst {nconst}")
            return db.query(NameBasics.knownForTitles).filter(NameBasics.nconst == nconst).first()
        
    def get_title_by_id(self, nconst: str, tconst: str) -> Optional[str]:
        with next(get_db()) as db:
            self.logger.info(f"Buscando título {tconst} para nconst {nconst}")
            return db.query(NameBasics.knownForTitles).filter(NameBasics.nconst == nconst).filter(NameBasics.knownForTitles.contains(tconst)).first()
    
    def get_professions(self, nconst: str) -> List[str]:
        with next(get_db()) as db:
            self.logger.info(f"Buscando profissões para nconst {nconst}")
            return db.query(NameBasics.primaryProfession).filter(NameBasics.nconst == nconst).first()
        