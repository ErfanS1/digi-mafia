from sqlalchemy.orm import Session
from abc import ABC


class Repository(ABC):
    def __init__(self, db: Session):
        self.dbModel = None
        self.db = db

    def getAll(self):
        return self.db.query(self.dbModel).all()

    def getById(self, id: int):
        return self.db.query(self.dbModel).filter(self.dbModel.id == id).first()
