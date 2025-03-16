from asyncpg import create_pool, Pool, Connection
import json

   
class PostgresAsyncConnectionContext:
    def __init__(self, pg: 'Postgres'):
        self.pg = pg
        self.connection = None

    async def __aenter__(self):
        self.connection = await self.pg.get_connection()
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.connection != None:
            await self.pg.release_connection(self.connection)


class Postgres:
    def __init__(self, app):
        app.async_db = self.async_db
        self.app = app
        self.async_connection_pool = None
        
    def async_db(self) -> PostgresAsyncConnectionContext:
        return PostgresAsyncConnectionContext(self)
    
    async def get_pool(self) -> Pool:
        if self.async_connection_pool == None:
            self.async_connection_pool = await create_pool(
                min_size = self.app.config['DB_MINCONN'],
                max_size = self.app.config['DB_MAXCONN'],
                host     = self.app.config['DB_HOST'],
                port     = self.app.config['DB_PORT'],
                user     = self.app.config['DB_USER'],
                password = self.app.config['DB_PASS'],
                database = self.app.config['DB_NAME']
            )
        return self.async_connection_pool
            
    async def get_connection(self) -> Connection:
        pool = await self.get_pool()
        conn: Connection = await pool.acquire()
        
        await conn.set_type_codec(
            typename = 'json',
            encoder  = json.dumps,
            decoder  = json.loads,
            schema   = 'pg_catalog'
        )
        
        await conn.set_type_codec(
            typename = 'jsonb',
            encoder  = Postgres._jsonb_encoder,
            decoder  = Postgres._jsonb_decoder,
            schema   = 'pg_catalog',
            format   = 'binary'
        )
        
        return conn
    
    async def release_connection(self, conn: Connection):
        pool = await self.get_pool()
        await pool.release(conn)
      
    @staticmethod  
    def _jsonb_encoder(json_data: dict) -> bytes:
        return b'\x01' + json.dumps(json_data).encode('utf-8')

    @staticmethod
    def _jsonb_decoder(json_blob: bytes) -> dict:
        return json.loads(json_blob[1:].decode('utf-8'))