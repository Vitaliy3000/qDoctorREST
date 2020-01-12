def logger(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(result)
        return result

    return wrapper


@logger
def personId(omsNumber, birthDate):
    return f"""
        SELECT personId
        FROM person
        WHERE
            omsNumber = '{omsNumber}'
            and birthDate = '{birthDate}'
    """


@logger
def insert_person(omsNumber, birthDate):
    return f"""
        INSERT INTO person(
            omsNumber,
            birthDate
        )
        VALUES(
            {omsNumber},
            '{birthDate}'
        )
    """


@logger
def select_appointments(omsNumber, birthDate):
    return f"""
        SELECT
            appointmentId,
            startTime,
            endTime,
            priority,
            doctor
        FROM
            appointment
            INNER JOIN person ON appointment.personId = person.personId
        WHERE
            person.omsNumber = '{omsNumber}'
            and person.birthDate = '{birthDate}'
    """


@logger
def delete_appointment(personId, appointmentId):
    return f"""
        DELETE
        FROM
            appointment
        WHERE
            personId = '{personId}'
            and appointmentId = '{appointmentId}'
    """


@logger
def insert_appointment(personId, startTime, endTime, priority, timestamp, doctor):
    return f"""
        INSERT INTO appointment(
            personId,
            startTime,
            endTime,
            priority,
            timestamp,
            doctor
        )
        VALUES(
            {personId},
            '{startTime}',
            '{endTime}',
            {priority},
            '{timestamp}',
            '{doctor}'
        )
    """


@logger
def update_appointment(
    appointmentId, personId, startTime, endTime, priority, timestamp
):
    return f"""
        UPDATE appointment SET
            startTime='{startTime}',
            endTime='{endTime}',
            priority={priority},
            timestamp='{timestamp}'
        WHERE
            personId={personId}
            and appointmentId={appointmentId}
    """
