from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class TitleRatings(SQLModel, table=True):
    __tablename__ = "title_ratings"

    tconst: str = Field(foreign_key="title_basics.tconst", primary_key=True, description="Chave estrangeira para TitleBasics")
    averageRating: float = Field(..., description="Média ponderada das avaliações")
    numVotes: int = Field(..., description="Número de votos recebidos")

    # Relação inversa com TitleBasics
    title: Optional["TitleBasics"] = Relationship(back_populates="rating")