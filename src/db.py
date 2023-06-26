import sqlalchemy as db
import os

from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

class Db:
    def __init__(self):

        # 'postgresql://doadmin:AVNS_IWGrvoLyWBBT_TaUS9-@db-postgresql-syd1-64992-do-user-13928987-0.b.db.ondigitalocean.com:25060/tl'
        conn_string = os.getenv("DATABASE_URL")

        engine = db.create_engine(conn_string)
        self.connection = engine.connect()

        Session = sessionmaker(bind=engine)
        self.session = Session()


    def save(self, doc):
        self.session.add(doc)
        self.session.commit()


    def load_all(self):
        documents = self.session.query(Document).all()
        return documents
