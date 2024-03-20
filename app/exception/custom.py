from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from app.web.prompts.response import PromptResponse
from app import constants



class CustomException(Exception):
    def __init__(self, message: str):
        self.name = message


    def already_exists(self, response, message):
        detail = PromptResponse(
            payload = response,
            message = constants.PROMPT_ALREADY_EXISTS,
            status = status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        raise HTTPException(status_code=500, detail=detail.dict())

    @staticmethod
    def raise_exception(status_code, message):

        raise HTTPException(status_code=status_code, detail=message)
