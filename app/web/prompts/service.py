from app.web.base.service import BaseService
from app.web.prompts.db_service import Prompt as PromptDBService

from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession



class Prompt(BaseService):
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
        prompt_db_service = PromptDBService(self.db_session)
        prompt = await prompt_db_service.insert_data(data)

        return prompt

    async def get(self, data: Any, *args, **kwargs) -> Dict:
        """
        functon returns user data from DB
        :param data:
        :param args:
        :param kwargs:
        :return Dict:
        """
        prompt_service = PromptDBService(self.db_session)
        prompt = await prompt_service.get_data_by_id(data)
        return prompt

    async def delete(self, prompt_id: Any, *args, **kwargs):
        """
        function to delete user from system
        :param prompt_id:
        :param args:
        :param kwargs:
        :return:
        """
        prompt_service = PromptDBService(self.db_session)
        prompt = await prompt_service.delete_data(prompt_id)
        return prompt

    async def update(self, prompt_id: Any, prompt: Any, *args, **kwargs):
        """
        function to update user.
        :param prompt_id:
        :param prompt
        :param args:
        :param kwargs:
        :return:
        """
        prompt_service = PromptDBService(self.db_session)
        await prompt_service.update_data(prompt_id, prompt)
        response = await prompt_service.get_data_by_id(prompt_id)
        return response

    async def get_list(self, searchParameters: Any, *args, **kwargs):
        """
        function to get list of all users
        :param searchParameters:
        :param args:
        :param kwargs:
        :return:
        """
        prompt_service = PromptDBService(self.db_session)
        pagination_data, prompt_list = await prompt_service.get_all_data(searchParameters)
        return pagination_data, prompt_list

    async def add_rating(self, prompt_id: Any, rating: Any, *args, **kwargs):
        """
        function to get list of all users
        :param data:
        :param args:
        :param kwargs:
        :return:
        """
        prompt_service = PromptDBService(self.db_session)
        if rating > 0:
            await prompt_service.add_rating(prompt_id, rating)
        response = await prompt_service.get_rating_details(prompt_id)
        return response