import uvicorn

from src.core import logger
from src.core.settings import settings


if __name__ == "__main__":
    logger.configure()

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=settings.backend.port,
        workers=settings.backend.workers,
        log_config=logger.LOGGING_CONFIG,
    )
