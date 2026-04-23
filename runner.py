import uvicorn
from dotenv import dotenv_values
from os import environ

from src.core import logger


if __name__ == "__main__":
    logger.configure()

    config_vals = dotenv_values(".env")
    for key in config_vals:
        if not environ.get(key):
            environ[key] = config_vals[key]

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=int(environ.get("BACKEND_PORT")),
        workers=int(environ.get("BACKEND_WORKERS")),
        log_config=logger.LOGGING_CONFIG,
    )
