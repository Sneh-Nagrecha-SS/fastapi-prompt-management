import uuid
from typing import Any, List, Dict

from sqlalchemy import DateTime, func, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.sql import text
from starlette import status
from starlette.exceptions import HTTPException
from fastapi_pagination import paginate
from app import constants
from app.helper.response_helper import BaseResponse
from app.web.base.db_service import DBService
from app.web.profile.schema import User
from app.exception import CustomException
from app.web.prompts.response import PromptResponse
from app.web.prompts.schema import PromptMaster, Ratings


class Prompt(DBService):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def prompt_exists_by_id(self, prompt_id):
        select_query = select(PromptMaster).where(PromptMaster.id == prompt_id)
        existing_prompt_result = await self.db_session.execute(select_query)
        existing_prompt = existing_prompt_result.scalars().first()
        if existing_prompt:
            return existing_prompt
        return False

    async def get_rating_details(self, prompt_id) -> Dict:
        rating_query = select(func.round(func.avg(Ratings.rating, ), 1), func.count(Ratings.rating)).group_by(
            Ratings.prompt_id).where(Ratings.prompt_id == prompt_id)
        avg_rating_result = await self.db_session.execute(rating_query)

        avg_rating = total_ratings = 0
        avg_rating_data = avg_rating_result.first()
        if avg_rating_data is not None:
            avg_rating, total_ratings = avg_rating_data

        response = dict([("avg_rating", avg_rating), ("total_ratings", total_ratings)])
        return response

    async def add_rating(self, prompt_id: Any, rating: Any, *args, **kwargs):
        ratings = Ratings()
        ratings.prompt_id = prompt_id
        ratings.rating = rating
        self.db_session.add(ratings)
        await self.db_session.commit()
        await self.db_session.refresh(ratings)
        rating_dict = ratings.__dict__
        return rating_dict

    async def prompt_title_exists(self, title) -> bool:
        select_query = select(PromptMaster).where(PromptMaster.title == title)
        existing_prompt_result = await self.db_session.execute(select_query)
        existing_prompt = list(existing_prompt_result.scalars())
        if existing_prompt:
            return True
        return False

    async def insert_data(self, data: Any, *args, **kwargs) -> Dict:
        """
        function to create user record in database and return dictionary
        :param data:
        :param args:
        :param kwargs:
        :return Dict:
        """

        if await self.prompt_title_exists(data.title):
            raise CustomException(message=constants.PROMPT_ALREADY_EXISTS)

        promptMaster = PromptMaster()

        promptMaster.id = uuid.uuid4()
        promptMaster.title = data.title
        promptMaster.description = data.description
        promptMaster.section = data.section
        promptMaster.tags = ",".join(data.tags)
        promptMaster.topic = data.topic
        promptMaster.created_at = func.now()

        self.db_session.add(promptMaster)
        await self.db_session.commit()
        await self.db_session.refresh(promptMaster)

        promptMaster_data_dict = promptMaster.__dict__
        promptMaster_data_dict.pop("_sa_instance_state")

        return promptMaster_data_dict

    async def get_data_by_id(self, prompt_id: Any, *args, **kwargs) -> Dict:
        """
        function to get single user by id
        :param _id:
        :param args:
        :param kwargs:
        :return Dict:
        """
        select_query = (select(PromptMaster.id, PromptMaster.title, PromptMaster.description, PromptMaster.topic, PromptMaster.section, PromptMaster.tags, PromptMaster.created_at, PromptMaster.updated_at,
                               func.coalesce(func.count(Ratings.prompt_id), 0).label("total_ratings"),
                               func.coalesce(func.avg(Ratings.rating), 0).label("avg_rating"))
                        .outerjoin(Ratings, PromptMaster.id == Ratings.prompt_id)
                        .where(PromptMaster.id == prompt_id)
                        .group_by(Ratings.prompt_id))

        prompt_result = await self.db_session.execute(select_query)
        prompt = prompt_result.mappings().one().items()
        print(prompt)
        if not prompt:
            raise CustomException(message=constants.PROMPT_NOT_DEFINED)
        prompt_dict = prompt
        #prompt_dict.pop("_sa_instance_state")
        return prompt_dict

    async def update_data(self, prompt_id: str, data: Any, *args, **kwargs) :
        """
        function to update user data in SQL database
        :prompt_id:
        :param data:
        :param args:
        :param kwargs:
        :return:
        """

        existing_prompt = await self.prompt_exists_by_id(prompt_id)

        if not existing_prompt:
            raise CustomException(message=constants.PROMPT_NOT_DEFINED)

        update_values = {}

        # Check if Title is provided
        if data.title is not None:
            # If title is provided check if it is not the same as earlier and there is no same title already
            if data.title != existing_prompt.title and await self.prompt_title_exists(data.title):
                    raise CustomException(message=constants.PROMPT_ALREADY_EXISTS)
            update_values["title"] = data.title

        if data.description is not None:
            update_values["description"] = data.description

        if data.section is not None:
            update_values["section"] = data.section

        if data.tags is not None:
            update_values["tags"] = ",".join(data.tags)

        if data.rating > 0:
            await self.add_rating(prompt_id, data.rating)

        if len(update_values) > 0:
            update_values["updated_at"] = func.now()
            update_query = update(PromptMaster).where(PromptMaster.id == prompt_id).values(update_values)
            await self.db_session.execute(update_query)
            await self.db_session.commit()

        return data.__dict__

    async def delete_data(self, prompt_id: Any, *args, **kwargs):
        """
        delete user data from SQL database
        :param data:
        :param args:
        :param kwargs:
        :return:
        """
        select_query = select(PromptMaster).where(PromptMaster.id == prompt_id)
        prompt_result = await self.db_session.execute(select_query)
        prompt = list(prompt_result.scalars())

        if not prompt:
            raise CustomException(message=constants.PROMPT_NOT_DEFINED)

        delete_query = delete(PromptMaster).where(PromptMaster.id == prompt_id)
        prompt_result = await self.db_session.execute(delete_query)
        return prompt_id

    async def get_all_data(self, searchParameters: Any, *args, **kwargs):
        """
        get list of user from SQL database.
        :param searchParameters:
        :param args:
        :param kwargs:
        :return:
        """
        query = select(PromptMaster.id, PromptMaster.title, PromptMaster.description, PromptMaster.topic, PromptMaster.section, PromptMaster.tags, PromptMaster.created_at, PromptMaster.updated_at,
                       func.coalesce(func.count(Ratings.prompt_id), 0).label("total_ratings"),
                       func.coalesce(func.avg(Ratings.rating), 0).label("avg_rating")).outerjoin(Ratings, Ratings.prompt_id == PromptMaster.id)
        if searchParameters.search:
             search_term = f"%{searchParameters.search}%"
             query = query.filter(or_(PromptMaster.title.ilike(search_term),
                              (PromptMaster.description.ilike(search_term))))

        if searchParameters.sort_by:
            sort_column = getattr(PromptMaster, searchParameters.sort_by)

            if searchParameters.sort_order == "ASC":
                query = query.order_by(sort_column.asc())
            else:
                query = query.order_by(sort_column.desc())

        query = query.group_by(PromptMaster.id)
        total_records = await self.db_session.scalar(select(func.count()).select_from(query))
        offset = (searchParameters.page_number - 1) * searchParameters.records_per_page
        query = query.offset(offset).limit(searchParameters.records_per_page)

        result = await self.db_session.execute(query)
        result_dict = [result for result in result.mappings().all()]
        return total_records, result_dict

