import uvicorn

from app.services.db.initialise_db import initialize_db
from app.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "app.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        factory=True,
    )

    initialize_db()



if __name__ == "__main__":
    main()
