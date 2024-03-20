from enum import Enum
from http.client import HTTPResponse
from fastapi import Depends
from fastapi_utils.inferring_router import InferringRouter
from pydantic import Field, BaseModel
from sqlalchemy import select
from starlette import status
from typing_extensions import Annotated, Optional
from typing import List
import app.constants
from app import constants
from app.services.db.dependency import get_db_session
from app.web.prompts.response import PromptResponse
from app.web.prompts.schema import PromptMaster
from app.web.prompts.service import Prompt as PromptService
from fastapi_pagination import paginate, add_pagination

from app.web.prompts.validator import PromptUpdate, PromptSearch, Prompt





router = InferringRouter()

@router.get('/')
async def get_prompt(prompt_id: str, db=Depends(get_db_session)) -> PromptResponse:
    prompt_service = PromptService(db)
    response = await prompt_service.get(prompt_id)
    return PromptResponse(
        payload=response,
        message=constants.PROMPT_GET_SUCCESS,
        status=status.HTTP_200_OK
    )


@router.post('/')
async def add_prompt(prompt_data: Prompt, db=Depends(get_db_session)) -> PromptResponse:
    prompt_service = PromptService(db)
    response = await prompt_service.create(prompt_data)

    # if prompt_data.rating > 0:
    response_rating = await prompt_service.add_rating(response["id"], prompt_data.rating)

    response.update(response_rating)

    return PromptResponse(
        payload=response,
        message=constants.PROMPT_CREATED_SUCCESS,
        status=status.HTTP_200_OK
    )


@router.delete('/')
async def delete_prompt(prompt_id: str, db=Depends(get_db_session)) -> PromptResponse:
    prompt_service = PromptService(db)
    response = await prompt_service.delete(prompt_id)

    return PromptResponse(
        message=constants.PROMPT_DELETED_SUCCESS,
        status=status.HTTP_200_OK
    )


@router.put('/')
async def update_prompt(prompt_id: str, prompt: PromptUpdate, db=Depends(get_db_session)):
    prompt_service = PromptService(db)
    response = await prompt_service.update(prompt_id, prompt)
    print(response)
    return PromptResponse(
        payload=response,
        message=constants.PROMPT_UPDATED_SUCCESS,
        status=status.HTTP_200_OK
    )

@router.post('/list')
async def get_list_of_prompts(searchParameters: PromptSearch, db=Depends(get_db_session)):
    prompt_service = PromptService(db)
    total_records, response = await prompt_service.get_list(searchParameters)

    pagination_data = dict([("total_records", total_records), ("page_number", searchParameters.page_number), ("records_per_page", searchParameters.records_per_page)])
    return response, pagination_data
