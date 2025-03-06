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

    def populate_title_basics(self, session: Session):
        data = self.load_csv(self.datasets["title_basics"])

        for row in data:
            title = TitleBasics(
                tconst=row["tconst"],
                titleType=row["titleType"],
                primaryTitle=row["primaryTitle"],
                originalTitle=row["originalTitle"],
                isAdult=row["isAdult"] == "1",
                startYear=int(row["startYear"]) if row["startYear"] != "\\N" else None,
                endYear=int(row["endYear"]) if row["endYear"] != "\\N" else None,
                runtimeMinutes=int(row["runtimeMinutes"]) if row["runtimeMinutes"] != "\\N" else None,
                genres=row["genres"] if row["genres"] != "\\N" else None
            )
            session.add(title)
        print("Títulos inseridos em title_basics.")

    def populate_title_ratings(self, session: Session):
        data = self.load_csv(self.datasets["title_ratings"])

        for row in data:
            rating = TitleRatings(
                tconst=row["tconst"],
                averageRating=float(row["averageRating"]),
                numVotes=int(row["numVotes"])
            )
            session.add(rating)
            session.commit()  # Commit após cada inserção
        print("Avaliações inseridas em title_ratings.")

    # def populate_title_crew(self, session: Session):
    #     data = self.load_csv(self.datasets["title_crew"])

    #     for row in data:
    #         crew = TitleCrew(
    #             tconst=row["tconst"],
    #             directors=row["directors"] if row["directors"] != "\\N" else None,
    #             writers=row["writers"] if row["writers"] != "\\N" else None
    #         )
    #         session.add(crew)
    #         session.commit()  # Commit após cada inserção
    #     print("Diretores e roteiristas inseridos em title_crew.")
    
    def populate_title_crew(self, session: Session):
        data = self.load_csv(self.datasets["title_crew"])

        for row in data:
            tconst = row["tconst"]
            existing_title = session.query(TitleBasics).filter(TitleBasics.tconst == tconst).first()

            if existing_title:  # Verifica se o tconst existe em title_basics
                crew = TitleCrew(
                    tconst=tconst,
                    directors=row["directors"] if row["directors"] != "\\N" else None,
                    writers=row["writers"] if row["writers"] != "\\N" else None
                )
                session.add(crew)
                session.commit()  # Commit após cada inserção
            else:
                print(f"Registro com tconst {tconst} não encontrado em title_basics. Ignorando.")
        print("Diretores e roteiristas inseridos em title_crew.")

    def populate_title_principals(self, session: Session):
        data_principals = self.load_csv(self.datasets["title_principals"])

        for row in data_principals:
            tconst = row["tconst"]
            nconst = row["nconst"]

            existing_title = session.query(TitleBasics).filter(TitleBasics.tconst == tconst).first()
            existing_name = session.query(NameBasics).filter(NameBasics.nconst == nconst).first()

            if existing_title and existing_name:  # Verifica se tconst e nconst existem
                principal = TitlePrincipals(
                    tconst=tconst,
                    ordering=int(row["ordering"]),
                    nconst=nconst,
                    category=row["category"],
                    job=row["job"] if row["job"] != "\\N" else None,
                    characters=row["characters"] if row["characters"] != "\\N" else None
                )
                session.add(principal)
                session.commit()  # Commit após cada inserção
            else:
                if not existing_title:
                    print(f"Registro com tconst {tconst} não encontrado em title_basics. Ignorando.")
                if not existing_name:
                    print(f"Registro com nconst {nconst} não encontrado em name_basics. Ignorando.")

        print("Profissionais inseridos em title_principals.")

        for row in data_principals:
            principal = TitlePrincipals(
                tconst=row["tconst"],
                ordering=int(row["ordering"]),
                nconst=row["nconst"],
                category=row["category"],
                job=row["job"] if row["job"] != "\\N" else None,
                characters=row["characters"] if row["characters"] != "\\N" else None
            )
            session.add(principal)
            session.commit()  # Commit após cada inserção

        print("Profissionais inseridos em title_principals e name_basics.")

    def run(self):
        with Session(engine) as session:
            self.populate_title_basics(session)
            self.populate_title_ratings(session)
            self.populate_title_crew(session)
            self.populate_title_principals(session)
            session.commit()

        print("Banco populado com sucesso!")


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    datasets = {
        "title_basics": os.path.join(BASE_DIR, "title.basics.csv"),
        "title_ratings": os.path.join(BASE_DIR, "title.ratings.csv"),
        "title_crew": os.path.join(BASE_DIR, "title.crew.csv"),
        "title_principals": os.path.join(BASE_DIR, "title.principals.csv"),
        "name_basics": os.path.join(BASE_DIR, "name.basics.csv")
    }

    service = IMDbDataService(datasets)
    service.run()
    