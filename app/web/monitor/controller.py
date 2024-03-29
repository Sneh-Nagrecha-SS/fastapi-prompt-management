from fastapi import Depends, status
from redis.asyncio import Redis
from app import logger
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from app.web.monitor.response import HealthResponse
from app import constants
from fastapi.requests import Request
from app.services.db.dependency import get_db_session


router = InferringRouter()


@cbv(router)
class Monitor:
    @router.get("/health")
    async def health_check(
        self,
        request: Request,
        db=Depends(get_db_session),

    ) -> HealthResponse:
        """
        Checks the health of a project.

        It returns 200 if the project is healthy.
        """
        await db.connection()

        logger.info("This is sample log")
        return HealthResponse(
            status=status.HTTP_200_OK, message=constants.HEALTH_SUCCESS, payload={}
        )
