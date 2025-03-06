from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from src.app.models.title_principals import TitlePrincipals


class NameBasics(SQLModel, table=True):
    __tablename__ = "name_basics"

    nconst: str = Field(primary_key=True, description="Identificador único da pessoa")
    primaryName: str = Field(..., description="Nome principal")
    birthYear: Optional[int] = Field(default=None, description="Ano de nascimento")
    deathYear: Optional[int] = Field(default=None, description="Ano de falecimento, se aplicável")
    primaryProfession: Optional[str] = Field(default=None, description="Principais profissões (separadas por vírgula)")
    knownForTitles: Optional[str] = Field(default=None, description="Títulos pelos quais a pessoa é conhecida")

    # Relação com TitlePrincipals (um nome pode ter diversas participações)
    principals: List["TitlePrincipals"] = Relationship(back_populates="name")

    # Relação N:M com TitleBasics via tabela de associação TitlePrincipals
    titles: List["TitleBasics"] = Relationship(back_populates="names", link_model=TitlePrincipals, sa_relationship_kwargs={"overlaps": "name, principals"})