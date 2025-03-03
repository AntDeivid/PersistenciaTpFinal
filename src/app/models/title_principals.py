from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class TitlePrincipals(SQLModel, table=True):
    __tablename__ = "title_principals"

    # Chave composta: (tconst, ordering)
    tconst: str = Field(foreign_key="title_basics.tconst", primary_key=True, description="Chave estrangeira para TitleBasics")
    ordering: int = Field(primary_key=True, description="Número de ordenação para o título")
    nconst: str = Field(foreign_key="name_basics.nconst", primary_key=True, description="Chave estrangeira para NameBasics")
    category: str = Field(..., description="Categoria do trabalho (ex.: actor, director)")
    job: Optional[str] = Field(default=None, description="Título específico do trabalho, se aplicável")
    characters: Optional[str] = Field(default=None, description="Personagem(s) interpretado(s), se aplicável")

    # Relação com TitleBasics
    title: Optional["TitleBasics"] = Relationship(back_populates="principals")
    # Relação com NameBasics
    name: Optional["NameBasics"] = Relationship(back_populates="principals")