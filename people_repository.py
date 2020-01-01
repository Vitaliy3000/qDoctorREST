import asyncio
import functools
import datetime
from connection import _get_connection


async def check(omsNumber, birthDate):
    query = f"""
    SELECT personId
    FROM person
    WHERE
        omsNumber = '{omsNumber}'
        and birthDate = '{birthDate}'
    """
    print(query)
    conn = await _get_connection()
    result = await conn.fetch(query)
    await conn.close()
    return bool(result)


async def _count_persons():
    query = f"""
    SELECT count(personId)
    FROM person
    """
    print(query)
    conn = await _get_connection()
    result = await conn.fetch(query)
    await conn.close()
    return result[0][0]


async def add(omsNumber, birthDate):
    birthDate = datetime.datetime.strptime(birthDate, "%Y-%m-%d").date()
    id = await _count_persons()
    query = (
        """INSERT INTO person(omsNumber, birthDate, personId, timestamp)
                VALUES($1, $2, $3, $4)""",
        omsNumber,
        birthDate,
        id + 1,
        datetime.datetime.now(),
    )
    print(query)
    conn = await _get_connection()
    await conn.execute(*query)
    await conn.close()