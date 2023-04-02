from typing import Optional

from Games import schemas
from database import enums
from database import db_models
from .repository import Repository


class RoleRepository(Repository):
    def __init__(self, db):
        super().__init__(db)
        self.dbModel = db_models.Role
