import csv
import os

from sqlmodel import Session

from src.app.core.db.database import engine
from src.app.models.name_basics import NameBasics
from src.app.models.title_basics import TitleBasics
from src.app.models.title_crew import TitleCrew
from src.app.models.title_principals import TitlePrincipals
from src.app.models.title_ratings import TitleRatings


class IMDbDataService:
    def __init__(self, datasets: dict):
        self.datasets = datasets

    def load_csv(self, filepath, delimiter="\t", limit=None):
        with open(filepath, encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=delimiter)
            data = list(reader)
            return data[:limit] if limit else data

    def populate_name_basics(self, session: Session):
        data = self.load_csv(self.datasets["name_basics"])

        for row in data:
            name_basic = NameBasics(
                nconst=row["nconst"],
                primaryName=row["primaryName"],
                birthYear=int(row["birthYear"]) if row["birthYear"] else None,
                deathYear=int(row["deathYear"]) if row["deathYear"] else None,
                primaryProfession=row["primaryProfession"] if row["primaryProfession"] else None,
                knownForTitles=row["knownForTitles"] if row["knownForTitles"] else None,
            )
            session.add(name_basic)
        print("Dados de nomes inseridos em name_basics.")
        session.commit() 


    def populate_title_basics(self, session: Session):
        data = self.load_csv(self.datasets["title_basics"])

        for row in data:
            title = TitleBasics(
                tconst=row["tconst"],
                titleType=row["titleType"],
                primaryTitle=row["primaryTitle"],
                originalTitle=row["originalTitle"],
                isAdult=row["isAdult"] == "1",
                startYear=int(row["startYear"]) if row["startYear"] else None,
                endYear=int(row["endYear"]) if row["endYear"] else None,
                runtimeMinutes=int(row["runtimeMinutes"]) if row["runtimeMinutes"] else None,
                genres=row["genres"] if row["genres"] else None
            )
            session.add(title)
        print("Títulos inseridos em title_basics.")
        session.commit()  


    def populate_title_ratings(self, session: Session):
        data = self.load_csv(self.datasets["title_ratings"])

        for row in data:
            rating = TitleRatings(
                tconst=row["tconst"],
                averageRating=float(row["averageRating"]),
                numVotes=int(row["numVotes"])
            )
            session.add(rating)
        print("Avaliações inseridas em title_ratings.")
        session.commit()  


    def populate_title_crew(self, session: Session):
        data = self.load_csv(self.datasets["title_crew"])

        for row in data:
            tconst = row["tconst"]
            existing_title = session.query(TitleBasics).filter(TitleBasics.tconst == tconst).first()

            if existing_title:  
                crew = TitleCrew(
                    tconst=tconst,
                    directors=row["directors"] if row["directors"] else None,
                    writers=row["writers"] if row["writers"] else None
                )
                session.add(crew)
            else:
                print(f"Registro com tconst {tconst} não encontrado em title_basics. Ignorando.")
        print("Diretores e roteiristas inseridos em title_crew.")
        session.commit() 


    def populate_title_principals(self, session: Session):
        data = self.load_csv(self.datasets["title_principals"])

        for row in data:
            tconst = row["tconst"]
            nconst = row["nconst"]

            existing_title = session.query(TitleBasics).filter(TitleBasics.tconst == tconst).first()
            existing_name = session.query(NameBasics).filter(NameBasics.nconst == nconst).first()

            if existing_title and existing_name:  
                try:
                    ordering = int(row["ordering"])
                except ValueError:
                    print(f"Valor inválido para 'ordering' em tconst {tconst}, nconst {nconst}. Ignorando registro.")
                    continue  

                principal = TitlePrincipals(
                    tconst=tconst,
                    ordering=ordering,
                    nconst=nconst,
                    category=row["category"],
                    job=row["job"] if row["job"] else None,
                    characters=row["characters"] if row["characters"] else None
                )
                session.add(principal)

            else:
                if not existing_title:
                    print(f"Registro com tconst {tconst} não encontrado em title_basics. Ignorando.")
                if not existing_name:
                    print(f"Registro com nconst {nconst} não encontrado em name_basics. Ignorando.")

        print("Profissionais inseridos em title_principals.")
        session.commit() 



    def run(self):
        with Session(engine) as session:
            self.populate_name_basics(session)
            self.populate_title_basics(session)
            self.populate_title_ratings(session)
            self.populate_title_crew(session)
            self.populate_title_principals(session)
            session.commit()

        print("Banco populado com sucesso!")


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    datasets = {
        "title_basics": os.path.join(BASE_DIR, "./filtrados/filtered_title.basics.tsv"),
        "title_ratings": os.path.join(BASE_DIR, "./filtrados/filtered_title.ratings.tsv"),
        "title_crew": os.path.join(BASE_DIR, "./filtrados/filtered_title.crew.tsv"),
        "title_principals": os.path.join(BASE_DIR, "./filtrados/filtered_title.principals.tsv"),
        "name_basics": os.path.join(BASE_DIR, "./filtrados/filtered_name.basics.tsv")
    }

    service = IMDbDataService(datasets)
    service.run()