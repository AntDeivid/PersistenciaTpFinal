import csv
import os

from sqlmodel import Session, select

from src.app.core.db.database import engine
from src.app.models.name_basics import NameBasics
from src.app.models.title_basics import TitleBasics
from src.app.models.title_crew import TitleCrew
from src.app.models.title_principals import TitlePrincipals
from src.app.models.title_ratings import TitleRatings


class IMDbDataService:
    def __init__(self, datasets: dict):
        self.datasets = datasets

    def load_csv(self, filepath, limit=None):
        with open(filepath, encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter="\t")
            data = list(reader)
            return data[:limit] if limit else data

    def populate_title_basics(self, session: Session):
        data = self.load_csv(self.datasets["title_basics"], limit=300)

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
        print("300 títulos inseridos em title_basics.")

    def populate_title_ratings(self, session: Session):
        data = self.load_csv(self.datasets["title_ratings"])
        existing_titles = {t.tconst for t in session.exec(select(TitleBasics)).all()}

        for row in data:
            tconst = row["tconst"]
            if tconst in existing_titles:
                rating = TitleRatings(
                    tconst=tconst,
                    averageRating=float(row["averageRating"]),
                    numVotes=int(row["numVotes"])
                )
                session.add(rating)
        print("Avaliações inseridas em title_ratings.")

    def populate_title_crew(self, session: Session):
        data = self.load_csv(self.datasets["title_crew"])
        existing_titles = {t.tconst for t in session.exec(select(TitleBasics)).all()}

        for row in data:
            tconst = row["tconst"]
            if tconst in existing_titles:
                crew = TitleCrew(
                    tconst=tconst,
                    directors=row["directors"] if row["directors"] != "\\N" else None,
                    writers=row["writers"] if row["writers"] != "\\N" else None
                )
                session.add(crew)
        print("Diretores e roteiristas inseridos em title_crew.")

    def populate_title_principals(self, session: Session):
        data_principals = self.load_csv(self.datasets["title_principals"])
        data_names = self.load_csv(self.datasets["name_basics"])
        existing_titles = {t.tconst for t in session.exec(select(TitleBasics)).all()}
        existing_people = {n.nconst for n in session.exec(select(NameBasics)).all()}

        for row in data_principals:
            tconst = row["tconst"]
            if tconst in existing_titles:
                nconst = row["nconst"]

                if nconst not in existing_people:
                    person_data = next((p for p in data_names if p["nconst"] == nconst), None)
                    if person_data:
                        person = NameBasics(
                            nconst=nconst,
                            primaryName=person_data["primaryName"],
                            birthYear=int(person_data["birthYear"]) if person_data["birthYear"] != "\\N" else None,
                            deathYear=int(person_data["deathYear"]) if person_data["deathYear"] != "\\N" else None,
                            primaryProfession=person_data["primaryProfession"] if person_data[
                                                                                      "primaryProfession"] != "\\N" else None,
                            knownForTitles=person_data["knownForTitles"] if person_data[
                                                                                "knownForTitles"] != "\\N" else None
                        )
                        session.add(person)
                        existing_people.add(nconst)

                principal = TitlePrincipals(
                    tconst=tconst,
                    ordering=int(row["ordering"]),
                    nconst=nconst,
                    category=row["category"],
                    job=row["job"] if row["job"] != "\\N" else None,
                    characters=row["characters"] if row["characters"] != "\\N" else None
                )
                session.add(principal)

        print("Profissionais inseridos em title_principals e name_basics.")

    def run(self):
        with Session(engine) as session:
            self.populate_title_basics(session)
            session.commit()

            self.populate_title_ratings(session)
            self.populate_title_crew(session)
            self.populate_title_principals(session)
            session.commit()

        print("Banco populado com sucesso!")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    datasets = {
        "title_basics": os.path.join(BASE_DIR, "title.basics.tsv"),
        "title_ratings": os.path.join(BASE_DIR, "title.ratings.tsv"),
        "title_crew": os.path.join(BASE_DIR, "title.crew.tsv"),
        "title_principals": os.path.join(BASE_DIR, "title.principals.tsv"),
        "name_basics": os.path.join(BASE_DIR, "name.basics.tsv")
    }

    service = IMDbDataService(datasets)
    service.run()
