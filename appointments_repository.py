import asyncio
import functools
import datetime
from connection import _get_connection

async def read(omsNumber, birthDate):
    query = f"""
    SELECT
        appointmentId,
        startTime,
        endTime,
        lpuId,
        code,
        availableResourceId,
        complexResourceId,
        priority
    FROM 
        person
        INNER JOIN
        appointment
        ON person.personId = appointment.personId
    WHERE
        omsNumber = '{omsNumber}'
        and birthDate = '{birthDate}'
    """
    print(query)
    conn = await _get_connection()
    rows = await conn.fetch(query)
    await conn.close()

    result = []
    for row in rows:
        row = dict(row)
        row['availableResourceId'] = row['availableResourceId'][1:-1]
        row['code'] = row['code'][1:-1]
        row['complexResourceId'] = row['complexResourceId'][1:-1]
        row['lpuId'] = row['lpuId'][1:-1]
        row['endTime'] = row['endTime'].strftime('%Y-%m-%dT%H:%M:%S')
        row['startTime'] = row['startTime'].strftime('%Y-%m-%dT%H:%M:%S')
        result.append(row)

    return result


async def delete(omsNumber, birthDate, appointmentId):
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

    query = f"""
    DELETE
    FROM
        appointment
    WHERE
        personId = '{result[0][0]}'
        and appointmentId = '{appointmentId}'
    """
    print(query)
    conn = await _get_connection()
    result = await conn.execute(query)
    await conn.close()


async def _count_appointments():
    query = f"""
    SELECT count(appointmentId)
    FROM appointment
    """
    print(query)
    conn = await _get_connection()
    result = await conn.fetch(query)
    await conn.close()
    return result[0][0]


async def add(omsNumber, birthDate, startTime, endTime, lpuId, code, availableResourceId, complexResourceId, priority):
    birthDate = datetime.datetime.strptime(birthDate, "%Y-%m-%d").date()
    startTime = datetime.datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%S")
    endTime = datetime.datetime.strptime(endTime, "%Y-%m-%dT%H:%M:%S")
    id = await _count_appointments()

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

    query = (
        """
        INSERT INTO appointment(
            appointmentId,
            personId,
            startTime,
            endTime,
            lpuId,
            code,
            availableResourceId,
            complexResourceId,
            priority,
            state,
            timestamp
        )
        VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        """,
        id+1,
        result[0][0],
        startTime,
        endTime,
        f'"{lpuId}"',
        f'"{code}"',
        f'"{availableResourceId}"',
        f'"{complexResourceId}"',
        priority,
        False,
        datetime.datetime.now(),
    )
    print(query)
    conn = await _get_connection()
    result = await conn.execute(*query)
    await conn.close()


async def update(omsNumber, birthDate, appointmentId, startTime, endTime, priority):
    birthDate = datetime.datetime.strptime(birthDate, "%Y-%m-%d").date()
    startTime = datetime.datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%S")
    endTime = datetime.datetime.strptime(endTime, "%Y-%m-%dT%H:%M:%S")

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

    query = (
        """
        UPDATE appointment SET
            startTime=$1,
            endTime=$2,
            priority=$3,
            timestamp=$4
        WHERE
            personId=$5
            and appointmentId=$6
        """,
        startTime,
        endTime,
        priority,
        datetime.datetime.now(),
        result[0][0],
        appointmentId
    )
    print(query)
    conn = await _get_connection()
    result = await conn.execute(*query)
    await conn.close()
