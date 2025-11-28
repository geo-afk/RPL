from app.api.database.database import DatabaseHandler, next_session
from app.models.user import User
from typing import Sequence



class UserService:

    def __init__(self):
        self.user_db = DatabaseHandler(next_session, User)

    async def get_users(self) -> Sequence[User]:
        users = self.user_db.get_all()
        return users


