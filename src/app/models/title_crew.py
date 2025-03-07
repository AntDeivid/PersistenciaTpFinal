from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class TitleCrew(SQLModel, table=True):
    __tablename__ = "title_crew"

    tconst: str = Field(foreign_key="title_basics.tconst", primary_key=True, description="Chave estrangeira para TitleBasics")
    directors: str = Field(..., description="Lista de diretores (IDs separados por vírgula)",nullable=True)
    writers: str = Field(..., description="Lista de roteiristas (IDs separados por vírgula)", nullable=True)

    # Relação inversa com TitleBasics
    title: Optional["TitleBasics"] = Relationship(back_populates="crew")