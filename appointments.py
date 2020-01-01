from config import web
import appointments_repository as repo
import people_repository


async def read(request):
    omsNumber = request.query["omsNumber"]
    birthDate = request.query["birthDate"]
    appointments = await repo.read(omsNumber, birthDate)
    return web.json_response(appointments)


async def create(request):
    data = await request.json()

    omsNumber = data["person"]["omsNumber"]
    birthDate = data["person"]["birthDate"]

    startTime = data["appointment"]["startTime"]
    endTime = data["appointment"]["endTime"]
    lpuId = data["appointment"]["lpuId"]
    code = data["appointment"]["code"]
    availableResourceId = data["appointment"]["availableResourceId"]
    complexResourceId = data["appointment"]["complexResourceId"]
    priority = data["appointment"].get("priority", 0)

    flag_exist = await people_repository.check(omsNumber, birthDate)
    if not flag_exist:
        # hidden creation person
        people_repository.add(omsNumber, birthDate)

    await repo.add(omsNumber, birthDate, startTime, endTime, lpuId, code, availableResourceId, complexResourceId, priority)
    return web.Response(text="Appointment is create", staus=201)


async def update(request):
    data = await request.json()
    appointmentId = int(request.match_info["appointmentId"])

    omsNumber = data["person"]["omsNumber"]
    birthDate = data["person"]["birthDate"]

    startTime = data["appointment"]["startTime"]
    endTime = data["appointment"]["endTime"]
    priority = data["appointment"].get("priority", 0)

    try:
        await repo.update(omsNumber, birthDate, appointmentId, startTime, endTime, priority)
    except:
        return web.Response(text="Appointment not found", status=404)
    else:
        return web.Response(text="Appointment update")


async def delete(request):
    omsNumber = request.query["omsNumber"]
    birthDate = request.query["birthDate"]
    appointmentId = request.match_info["appointmentId"]

    try:
        await repo.delete(omsNumber, birthDate, appointmentId)
    except:
        return web.Response(text="Person not found", status=404)
    else:
        return web.Response(text=f"Appointment {appointmentId} deleted")
