from redis.asyncio import Redis

from app.config import database_settings

_token_blacklist=Redis(
    host=database_settings.REDIS_HOST,
    port=database_settings.REDIS_PORT,
    db=0
)

async def add_jti_to_blacklist(jti:str):
    await _token_blacklist.set(jti,"blacklisted")

async def is_jti_blacklisted(jti:str)->bool:
    return await _token_blacklist.exists(jti)