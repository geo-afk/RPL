from app.api.database.database import DatabaseHandler, next_session
from app.models.resource import Resource
from typing import Sequence


class ResourceService:

    def __init__(self):
        self.resource_db = DatabaseHandler(next_session, Resource)

    async def get_resources(self) -> Sequence[Resource]:
        all_resources = self.resource_db.get_all()
        return all_resources


