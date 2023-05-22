import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'

    id = db.Column('id', db.Integer, primary_key=True)
    filename = db.Column('filename', db.String(100), nullable=False)
    doc_hash = db.Column('doc_hash', db.String(100), nullable=False)


    def __init__(self, filename, doc_hash):
        self.filename = filename
        self.doc_hash = doc_hash


    def __repr__(self):
        return f'<Document {self.filename} {self.doc_hash}>'
    
