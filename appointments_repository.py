import asyncio
import functools
import datetime
from connection import _get_connection

async def read(oms_number, birth_date):
    query = f"""
    SELECT
        appointment_id,
        start_time,
        finish_time,
        lpu_id,
        code,
        available_resource_id,
        complex_resource_id,
        priority
    FROM 
        person
        INNER JOIN
        appointment
        ON person.person_id = appointment.person_id
    WHERE
        oms_number = '{oms_number}'
        and birth_date = '{birth_date}'
    """
    print(query)
    conn = await _get_connection()
    rows = await conn.fetch(query)
    await conn.close()

    result = []
    for row in rows:
        row = dict(row)
        row['available_resource_id'] = row['available_resource_id'][1:-1]
        row['code'] = row['code'][1:-1]
        row['complex_resource_id'] = row['complex_resource_id'][1:-1]
        row['lpu_id'] = row['lpu_id'][1:-1]
        row['finish_time'] = row['finish_time'].strftime('%Y-%m-%dT%H:%M:%S')
        row['start_time'] = row['start_time'].strftime('%Y-%m-%dT%H:%M:%S')
        result.append(row)

    return result


async def delete(oms_number, birth_date, appointment_id):
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

    query = f"""
    DELETE
    FROM
        appointment
    WHERE
        person_id = '{result[0][0]}'
        and appointment_id = '{appointment_id}'
    """
    print(query)
    conn = await _get_connection()
    result = await conn.execute(query)
    await conn.close()


async def _count_appointments():
    query = f"""
    SELECT count(appointment_id)
    FROM appointment
    """
    print(query)
    conn = await _get_connection()
    result = await conn.fetch(query)
    await conn.close()
    return result[0][0]


async def add(oms_number, birth_date, start_time, finish_time, lpu_id, code, available_resource_id, complex_resource_id, priority):
    birth_date = datetime.datetime.strptime(birth_date, "%Y-%m-%d").date()
    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
    finish_time = datetime.datetime.strptime(finish_time, "%Y-%m-%dT%H:%M:%S")
    id = await _count_appointments()

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

    query = (
        """
        INSERT INTO appointment(
            appointment_id,
            person_id,
            start_time,
            finish_time,
            lpu_id,
            code,
            available_resource_id,
            complex_resource_id,
            priority,
            state,
            timestamp
        )
        VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        """,
        id+1,
        result[0][0],
        start_time,
        finish_time,
        f'"{lpu_id}"',
        f'"{code}"',
        f'"{available_resource_id}"',
        f'"{complex_resource_id}"',
        priority,
        False,
        datetime.datetime.now(),
    )
    print(query)
    conn = await _get_connection()
    result = await conn.execute(*query)
    await conn.close()


async def update(oms_number, birth_date, appointment_id, start_time, finish_time, priority):
    birth_date = datetime.datetime.strptime(birth_date, "%Y-%m-%d").date()
    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
    finish_time = datetime.datetime.strptime(finish_time, "%Y-%m-%dT%H:%M:%S")

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

    query = (
        """
        UPDATE appointment SET
            start_time=$1,
            finish_time=$2,
            priority=$3,
            timestamp=$4
        WHERE
            person_id=$5
            and appointment_id=$6
        """,
        start_time,
        finish_time,
        priority,
        datetime.datetime.now(),
        result[0][0],
        appointment_id
    )
    print(query)
    conn = await _get_connection()
    result = await conn.execute(*query)
    await conn.close()
