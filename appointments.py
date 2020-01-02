from config import web
import repository as repo


async def read(request):
    omsNumber = request.query["omsNumber"]
    birthDate = request.query["birthDate"]
    appointments = await repo.read_all_appointments(omsNumber, birthDate)
    return web.json_response(appointments)


async def create(request):
    data = await request.json()

    omsNumber = data["person"]["omsNumber"]
    birthDate = data["person"]["birthDate"]

    startTime = data["appointment"]["startTime"]
    endTime = data["appointment"]["endTime"]
    doctor = data["appointment"]["doctor"]
    priority = data["appointment"].get("priority", 0)

    flag_exist = await repo.check_person(omsNumber, birthDate)
    if not flag_exist:
        # hidden creation person
        await repo.add_person(omsNumber, birthDate)

    await repo.add_appointment(omsNumber, birthDate, startTime, endTime, priority, doctor)
    return web.Response(text="Appointment is create", status=201)


async def update(request):
    data = await request.json()
    appointmentId = request.match_info["appointmentId"]

    omsNumber = data["person"]["omsNumber"]
    birthDate = data["person"]["birthDate"]

    startTime = data["appointment"]["startTime"]
    endTime = data["appointment"]["endTime"]
    priority = data["appointment"].get("priority", 0)

    try:
        await repo.update_appointment(omsNumber, birthDate, appointmentId, startTime, endTime, priority)
    except:
        return web.Response(text="Appointment not found", status=404)
    else:
        return web.Response(text="Appointment update")


async def delete(request):
    omsNumber = request.query["omsNumber"]
    birthDate = request.query["birthDate"]
    appointmentId = request.match_info["appointmentId"]

    try:
        await repo.delete_appointment(omsNumber, birthDate, appointmentId)
    except:
        return web.Response(text="Person not found", status=404)
    else:
        return web.Response(text=f"Appointment {appointmentId} deleted")
