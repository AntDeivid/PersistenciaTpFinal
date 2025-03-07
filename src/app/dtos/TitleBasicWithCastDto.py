from typing import List, Optional
from pydantic import BaseModel

class NameBasicsSchema(BaseModel):
    nconst: str
    primaryName: str

class TitlePrincipalsSchema(BaseModel):
    category: str
    job: Optional[str]
    name: NameBasicsSchema # Usando o esquema para NameBasics

class TitleRatingsSchema(BaseModel):
    averageRating: float
    numVotes: int

class TitleBasicsWithCast(BaseModel):
    tconst: str
    titleType: str
    primaryTitle: str
    originalTitle: str
    isAdult: bool
    startYear: Optional[int]
    endYear: Optional[int]
    runtimeMinutes: Optional[int]
    genres: Optional[str]
    rating: Optional[TitleRatingsSchema] = None # Usando o esquema para TitleRatings
    principals: List[TitlePrincipalsSchema] = []  # Lista de TitlePrincipals com NameBasics