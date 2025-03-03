from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from src.app.models.title_principals import TitlePrincipals


class TitleBasics(SQLModel, table=True):
    __tablename__ = "title_basics"

    tconst: str = Field(primary_key=True, description="Identificador único do título")
    titleType: str = Field(..., description="Tipo ou formato do título (ex.: movie, short, tvseries)")
    primaryTitle: str = Field(..., description="Título principal")
    originalTitle: str = Field(..., description="Título original")
    isAdult: bool = Field(..., description="Indica se é título adulto (True/False)")
    startYear: Optional[int] = Field(default=None, description="Ano de início (lançamento)")
    endYear: Optional[int] = Field(default=None, description="Ano de término, se aplicável")
    runtimeMinutes: Optional[int] = Field(default=None, description="Duração em minutos")
    genres: Optional[str] = Field(default=None, description="Gêneros (lista separada por vírgula)")

    # Relação 1:1 com TitleRatings
    rating: Optional["TitleRatings"] = Relationship(back_populates="title", sa_relationship_kwargs={"uselist": False})

    # Relação 1:1 com TitleCrew
    crew: Optional["TitleCrew"] = Relationship(back_populates="title", sa_relationship_kwargs={"uselist": False})

    # Relação 1:N com TitlePrincipals (um título pode ter vários profissionais)
    principals: List["TitlePrincipals"] = Relationship(back_populates="title")

    # Relação N:M com NameBasics via tabela de associação TitlePrincipals
    names: List["NameBasics"] = Relationship(back_populates="titles", link_model=TitlePrincipals)