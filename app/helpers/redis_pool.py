import asyncio_redis


class RedisAsyncConnectionContext:
    def __init__(self, rp: 'RedisPool'):
        self.rp = rp

    async def __aenter__(self) -> asyncio_redis.Pool:
        return await self.rp.get_pool()
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


class RedisPool:
    def __init__(self, app):
        app.async_redis = self.async_redis
        app.async_redis_pool = self
        self.app = app
        self.redis_connection_pool = None
        
    def async_redis(self) -> RedisAsyncConnectionContext:
        return RedisAsyncConnectionContext(self)
    
    async def get_pool(self) -> asyncio_redis.Pool:
        if self.redis_connection_pool == None:
            self.redis_connection_pool = await asyncio_redis.Pool.create(
                host     = self.app.config['REDIS_HOST'], 
                port     = self.app.config['REDIS_PORT'], 
                password = self.app.config['REDIS_PASS'],
                poolsize = self.app.config['REDIS_CONN']
            )
        return self.redis_connection_pool