from sqlalchemy.orm import Session
from app.database import db_models


def getUserWithEmail(email: str, db: Session) -> db_models.User:
    user = db.query(db_models.User).filter(db_models.User.email == email).first()

    return user
