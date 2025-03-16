from . import module
from quart import current_app, render_template
from ..helpers.utils import time_ms, time_us, time_ns
import asyncio


@module.get('/')
async def tests_page():
    return await render_template('tests.html')


async def test_redis_set_worker(start_ms: int, range_from: int, range_to: int) -> dict:
    timings = {}
    async with current_app.async_redis() as redis:
        for i in range(range_from, range_to):
            if ((i + 1) % 10 == 0) or (i == 0):
                start = time_ns()
                await redis.set(f'something_key:{i}', f'something_value:{i}')
                end = time_ns()
                    
                timings[time_ms() - start_ms] = end - start
            else:
                await redis.set(f'something_key:{i}', f'something_value:{i}')
    
    return timings


async def test_redis_get_worker(start_ms: int, range_from: int, range_to: int) -> dict:
    timings = {}
    async with current_app.async_redis() as redis:
        for i in range(range_from, range_to):
            if ((i + 1) % 10 == 0) or (i == 0):
                start = time_ns()
                await redis.get(f'something_key:{i}')
                end = time_ns()
                    
                timings[time_ms() - start_ms] = end - start
            else:
                await redis.get(f'something_key:{i}')
    
    return timings


async def test_redis_get_by_mask_worker(start_ms: int, range_from: int, range_to: int) -> dict:
    timings = {}
    async with current_app.async_redis() as redis:
        for i in range(range_from, range_to):
            if ((i + 1) % 10 == 0) or (i == 0):
                start = time_ns()
                await redis.get(f's*{i}')
                end = time_ns()
                    
                timings[time_ms() - start_ms] = end - start
            else:
                await redis.get(f's*{i}')
    
    return timings


@module.get('/test/redis')
async def test_redis():
    #
    #  Redis Flush
    #
    async with current_app.async_redis() as redis:
        await redis.flushall()
        
    #
    #  Redis Test 1: Insert
    #
    test_1_timings = {}
    test_1_start = time_ms()
        
    list_of_timings = await asyncio.gather(*[
        test_redis_set_worker(test_1_start, i * 2000, (i + 1) * 2000)
        for i in range(50)
    ])
        
    test_1_end = time_ms()
    test_1_total = test_1_end - test_1_start
     
    for t in list_of_timings:
        test_1_timings.update(t)
        
    #
    #  Redis Test 2: Update
    #
    test_2_timings = {}
    test_2_start = time_ms()
        
    list_of_timings = await asyncio.gather(*[
        test_redis_set_worker(test_2_start, (49 - i) * 2000, (49 - i + 1) * 2000)
        for i in range(50)
    ])
        
    test_2_end = time_ms()
    test_2_total = test_2_end - test_2_start
     
    for t in list_of_timings:
        test_2_timings.update(t)
        
    #
    #  Redis Test 3: Get
    #
    test_3_timings = {}
    test_3_start = time_ms()
        
    list_of_timings = await asyncio.gather(*[
        test_redis_get_worker(test_3_start, (49 - i) * 2000, (49 - i + 1) * 2000)
        for i in range(50)
    ])
        
    test_3_end = time_ms()
    test_3_total = test_3_end - test_3_start
     
    for t in list_of_timings:
        test_3_timings.update(t)
        
    #
    #  Redis Test 4: Get by mask
    #
    test_4_timings = {}
    test_4_start = time_ms()
        
    list_of_timings = await asyncio.gather(*[
        test_redis_get_by_mask_worker(test_4_start, (49 - i) * 2000, (49 - i + 1) * 2000)
        for i in range(50)
    ])
        
    test_4_end = time_ms()
    test_4_total = test_4_end - test_4_start
     
    for t in list_of_timings:
        test_4_timings.update(t)
        
    #
    #  Redis Flush
    #
    async with current_app.async_redis() as redis:
        await redis.flushall()
            
            
    return {
        'redis_insert'      : test_1_timings,
        'redis_insert_total': test_1_total,
        'redis_update'      : test_2_timings,
        'redis_update_total': test_2_total,
        'redis_get'         : test_3_timings,
        'redis_get_total'   : test_3_total,
        'redis_get_m'       : test_4_timings,
        'redis_get_m_total' : test_4_total,
    }
    
    
    
async def test_postgres_insert_worker(start_ms: int, range_from: int, range_to: int) -> dict:
    timings = {}
    async with current_app.async_db() as connection:
        for i in range(range_from, range_to):
            if ((i + 1) % 10 == 0) or (i == 0):
                start = time_ns()
                await connection.execute('INSERT INTO cache VALUES ($1, $2);', f'something_key:{i}', f'something_value:{i}')
                end = time_ns()
                    
                timings[time_ms() - start_ms] = end - start
            else:
                await connection.execute('INSERT INTO cache VALUES ($1, $2);', f'something_key:{i}', f'something_value:{i}')
    
    return timings


async def test_postgres_update_worker(start_ms: int, range_from: int, range_to: int) -> dict:
    timings = {}
    async with current_app.async_db() as connection:
        for i in range(range_from, range_to):
            if ((i + 1) % 10 == 0) or (i == 0):
                start = time_ns()
                await connection.execute('UPDATE cache SET value=$2 WHERE key=$1;', f'something_key:{i}', f'something_value:{i}')
                end = time_ns()
                    
                timings[time_ms() - start_ms] = end - start
            else:
                await connection.execute('UPDATE cache SET value=$2 WHERE key=$1;', f'something_key:{i}', f'something_value:{i}')
    
    return timings


async def test_postgres_select_worker(start_ms: int, range_from: int, range_to: int) -> dict:
    timings = {}
    async with current_app.async_db() as connection:
        for i in range(range_from, range_to):
            if ((i + 1) % 10 == 0) or (i == 0):
                start = time_ns()
                await connection.fetchrow('SELECT value FROM cache WHERE key=$1;', f'something_key:{i}')
                end = time_ns()
                    
                timings[time_ms() - start_ms] = end - start
            else:
                await connection.fetchrow('SELECT value FROM cache WHERE key=$1;', f'something_key:{i}')
    
    return timings


async def test_postgres_select_by_mask_worker(start_ms: int, range_from: int, range_to: int) -> dict:
    timings = {}
    async with current_app.async_db() as connection:
        for i in range(range_from, range_to):
            if ((i + 1) % 10 == 0) or (i == 0):
                start = time_ns()
                await connection.fetchrow("SELECT value FROM cache WHERE key LIKE $1;", f's%{i}')
                end = time_ns()
                    
                timings[time_ms() - start_ms] = end - start
            else:
                await connection.fetchrow("SELECT value FROM cache WHERE key LIKE $1;", f's%{i}')
    
    return timings


@module.get('/test/postgres')
async def test_postgres():
    #
    #  Init table
    #
    async with current_app.async_db() as connection:
        await connection.execute(
            '''
                DROP TABLE IF EXISTS cache;
                CREATE UNLOGGED TABLE cache(key character varying NOT NULL, value character varying NOT NULL);
                ALTER TABLE cache SET (AUTOVACUUM_ENABLED=FALSE);
                CREATE INDEX ON cache (key);
            '''
        )
        
    #
    #  Postgres Test 1: Insert
    #
    test_1_timings = {}
    test_1_start = time_ms()
        
    list_of_timings = await asyncio.gather(*[
        test_postgres_insert_worker(test_1_start, i * 2000, (i + 1) * 2000)
        for i in range(50)
    ])
        
    test_1_end = time_ms()
    test_1_total = test_1_end - test_1_start
     
    for t in list_of_timings:
        test_1_timings.update(t)
        
    #
    #  Postgres Test 2: Update
    #
    test_2_timings = {}
    test_2_start = time_ms()
        
    list_of_timings = await asyncio.gather(*[
        test_postgres_update_worker(test_2_start, (49 - i) * 2000, (49 - i + 1) * 2000)
        for i in range(50)
    ])
        
    test_2_end = time_ms()
    test_2_total = test_2_end - test_2_start
     
    for t in list_of_timings:
        test_2_timings.update(t)
        
    #
    #  Postgres Test 3: Select
    #
    test_3_timings = {}
    test_3_start = time_ms()
        
    list_of_timings = await asyncio.gather(*[
        test_postgres_select_worker(test_3_start, (49 - i) * 2000, (49 - i + 1) * 2000)
        for i in range(50)
    ])
        
    test_3_end = time_ms()
    test_3_total = test_3_end - test_3_start
     
    for t in list_of_timings:
        test_3_timings.update(t)
        
    #
    #  Postgres Test 4: Select Like
    #
    '''
    test_4_timings = {}
    test_4_start = time_ms()
        
    list_of_timings = await asyncio.gather(*[
        test_postgres_select_by_mask_worker(test_4_start, (49 - i) * 2000, (49 - i + 1) * 2000)
        for i in range(50)
    ])
        
    test_4_end = time_ms()
    test_4_total = test_4_end - test_4_start
     
    for t in list_of_timings:
        test_4_timings.update(t)
    '''
        
    #
    #  Drop table
    #
    async with current_app.async_db() as connection:
        await connection.execute('DROP TABLE IF EXISTS cache;')
            
            
    return {
        'pg_insert'        : test_1_timings,
        'pg_insert_total'  : test_1_total,
        'pg_update'        : test_2_timings,
        'pg_update_total'  : test_2_total,
        'pg_select'        : test_3_timings,
        'pg_select_total'  : test_3_total,
        #'pg_select_m'      : test_4_timings,
        #'pg_select_m_total': test_4_total,
    }