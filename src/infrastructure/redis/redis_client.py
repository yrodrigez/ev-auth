
from functools import lru_cache
from redis import Redis
from src.infrastructure.environment.environment import get_environment

@lru_cache
def get_redis_client() -> Redis:
    environment = get_environment()

    password = None

    if environment.redis_password is not None:
        password = environment.redis_password.get_secret_value() or None

    return Redis(
        host=environment.redis_host,
        port=environment.redis_port,
        password=password,
        decode_responses=True
    )
