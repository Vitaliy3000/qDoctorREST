import os
import asyncpg
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


async def _get_connection():
    return await asyncpg.connect(os.environ["DATABASE_URL"], ssl=ctx)
