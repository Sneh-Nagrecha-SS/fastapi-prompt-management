from app.web.base.service import BaseService
from app.web.profile.db_service import Profile as ProfileDBService

from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession



class Profile(BaseService):
    def __init__(
        self,
        db_session: AsyncSession = None,
    ):
        self.db_session = db_session

    async def create(self, data: Any, *args, **kwargs) -> Dict:
        """
        function to store user data in DB, indexes data in ES and set data in Redis
        :param data:
        :param args:
        :param kwargs:
        :return Dict:
        """
        profile_db_service = ProfileDBService(self.db_session)
        user = await profile_db_service.insert_data(data)


        return user

    async def get(self, data: Any, *args, **kwargs) -> Dict:
        """
        functon returns user data from DB
        :param data:
        :param args:
        :param kwargs:
        :return Dict:
        """
        profile_service = ProfileDBService(self.db_session)
        user = await profile_service.get_data_by_id(data)
        return user

    async def delete(self, data: Any, *args, **kwargs):
        """
        function to delete user from system
        :param data:
        :param args:
        :param kwargs:
        :return:
        """

    async def update(self, data: Any, *args, **kwargs):
        """
        function to update user.
        :param data:
        :param args:
        :param kwargs:
        :return:
        """
        pass

    async def get_list(self, data: Any, *args, **kwargs):
        """
        function to get list of all users
        :param data:
        :param args:
        :param kwargs:
        :return:
        """
