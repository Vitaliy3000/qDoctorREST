import asyncio
import functools
import datetime
from connection import _get_connection


async def check(oms_number, birth_date):
    query = f"""
    SELECT person_id
    FROM person
    WHERE
        oms_number = '{oms_number}'
        and birth_date = '{birth_date}'
    """
    print(query)
    conn = await _get_connection()
    result = await conn.fetch(query)
    await conn.close()
    return bool(result)


async def _count_persons():
    query = f"""
    SELECT count(person_id)
    FROM person
    """
    print(query)
    conn = await _get_connection()
    result = await conn.fetch(query)
    await conn.close()
    return result[0][0]


async def add(oms_number, birth_date):
    birth_date = datetime.datetime.strptime(birth_date, "%Y-%m-%d").date()
    id = await _count_persons()
    query = (
        """INSERT INTO person(oms_number, birth_date, person_id, timestamp)
                VALUES($1, $2, $3, $4)""",
        oms_number,
        birth_date,
        id + 1,
        datetime.datetime.now(),
    )
    print(query)
    conn = await _get_connection()
    await conn.execute(*query)
    await conn.close()