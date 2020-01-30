import getpass

import aiopg
import aiopg.sa
import asyncio


async def get_engine(dsn=None):
    dsn = dsn or 'postgres://{0}:{0}@127.0.0.1:5432'.format(getpass.getuser())
    return await aiopg.sa.create_engine(dsn)


async def txn_and_wait():
    async with (await get_engine()).acquire() as conn, conn.begin():
        print((await (await conn.execute("SELECT 1")).fetchone())[0])
        await asyncio.sleep(99999)


loop = asyncio.get_event_loop()
future = loop.create_task(txn_and_wait())

try:
    pending = asyncio.Task.all_tasks()
    loop.run_until_complete(asyncio.gather(*pending))
except KeyboardInterrupt:
    future.cancel()

pending = asyncio.Task.all_tasks()
loop.run_until_complete(asyncio.gather(*pending))
