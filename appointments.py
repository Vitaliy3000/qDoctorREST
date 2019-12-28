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

    start_time = data["appointment"]["start_time"]
    finish_time = data["appointment"]["finish_time"]
    lpu_id = data["appointment"]["lpu_id"]
    code = data["appointment"]["code"]
    available_resource_id = data["appointment"]["available_resource_id"]
    complex_resource_id = data["appointment"]["complex_resource_id"]
    priority = data["appointment"].get("priority", 0)

    flag_exist = await people_repository.check(omsNumber, birthDate)
    if not flag_exist:
        # hidden creation person
        people_repository.add(omsNumber, birthDate)

    await repo.add(omsNumber, birthDate, start_time, finish_time, lpu_id, code, available_resource_id, complex_resource_id, priority)
    return web.Response(text="Appointment is create", staus=201)


async def update(request):
    data = await request.json()
    appointment_id = int(request.match_info["appointment_id"])

    omsNumber = data["person"]["omsNumber"]
    birthDate = data["person"]["birthDate"]

    start_time = data["appointment"]["start_time"]
    finish_time = data["appointment"]["finish_time"]
    priority = data["appointment"].get("priority", 0)

    try:
        await repo.update(omsNumber, birthDate, appointment_id, start_time, finish_time, priority)
    except:
        return web.Response(text="Appointment not found", status=404)
    else:
        return web.Response(text="Appointment update")


async def delete(request):
    omsNumber = request.query["omsNumber"]
    birthDate = request.query["birthDate"]
    appointment_id = request.match_info["appointment_id"]

    try:
        await repo.delete(omsNumber, birthDate, appointment_id)
    except:
        return web.Response(text="Person not found", status=404)
    else:
        return web.Response(text=f"Appointment {appointment_id} deleted")
