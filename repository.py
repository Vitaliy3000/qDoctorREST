import datetime
import json

from connection import _get_connection
import query


async def check_person(omsNumber, birthDate):
    try:
        await _personId(omsNumber, birthDate)
    except AssertionError:
        return False
    else:
        return True


async def _personId(omsNumber, birthDate):
    conn = await _get_connection()
    result = await conn.fetch(query.personId(omsNumber, birthDate))
    await conn.close()
    assert result, 'Person is not exist'
    return result[0][0]


async def add_person(omsNumber, birthDate):
    conn = await _get_connection()
    result = await conn.execute(query.insert_person(
        omsNumber=omsNumber,
        birthDate=datetime.datetime.strptime(birthDate, "%Y-%m-%d").date(),
    ))
    await conn.close()


async def read_all_appointments(omsNumber, birthDate):
    conn = await _get_connection()
    rows = await conn.fetch(query.select_appointments(omsNumber, birthDate))
    await conn.close()

    result = []
    for row in rows:
        row = dict(row)
        row['appointmentId'] = row.pop('appointmentid')
        row['endTime'] = row.pop('endtime').strftime('%Y-%m-%dT%H:%M:%S')
        row['startTime'] = row.pop('starttime').strftime('%Y-%m-%dT%H:%M:%S')
        row['doctor'] = json.loads(row['doctor'])
        result.append(row)

    return result


async def delete_appointment(omsNumber, birthDate, appointmentId):
    conn = await _get_connection()
    result = await conn.execute(query.delete_appointment(
                                    await _personId(omsNumber, birthDate),
                                    int(appointmentId)))
    await conn.close()


async def add_appointment(omsNumber, birthDate, startTime, endTime, priority, doctor):
    conn = await _get_connection()
    result = await conn.execute(query.insert_appointment(
        personId=await _personId(omsNumber, birthDate),
        startTime=datetime.datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%S"),
        endTime=datetime.datetime.strptime(endTime, "%Y-%m-%dT%H:%M:%S"),
        priority=priority,
        timestamp=datetime.datetime.now(),
        doctor=json.dumps(doctor),
    ))
    await conn.close()


async def update_appointment(omsNumber, birthDate, appointmentId, startTime, endTime, priority):
    conn = await _get_connection()
    result = await conn.execute(query.update_appointment(
        appointmentId=int(appointmentId),
        personId=await _personId(omsNumber, birthDate),
        startTime=datetime.datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%S"),
        endTime=datetime.datetime.strptime(endTime, "%Y-%m-%dT%H:%M:%S"),
        priority=priority,
        timestamp=datetime.datetime.now(),
    ))
    await conn.close()