from datetime import datetime, timedelta

from src.infrastructure.config.settings import settings


def get_expiration_time() -> int:
    now = datetime.now()
    target = now.replace(
        hour=settings.redis.expiration_at.hour,
        minute=settings.redis.expiration_at.minute,
    )

    if now > target:
        target += timedelta(days=1)

    return int(target.timestamp())
