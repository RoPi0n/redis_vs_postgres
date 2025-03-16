class Config:
    DB_MINCONN = 50
    DB_MAXCONN = 50
        
    DB_HOST = 'localhost'
    DB_PORT = 5432
    DB_NAME = 'perfomance_test'
    DB_USER = 'postgres'
    DB_PASS = 'postgres'
    
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_PASS = ''
    REDIS_CONN = 50