from config import web
import appointments_repository as repo
import people_repository


async def read(request):
    oms_number = request.query["oms_number"]
    birth_date = request.query["birth_date"]
    appointments = await repo.read(oms_number, birth_date)
    return web.json_response(appointments)


async def create(request):
    data = await request.json()

    oms_number = data["person"]["oms_number"]
    birth_date = data["person"]["birth_date"]

    start_time = data["appointment"]["start_time"]
    finish_time = data["appointment"]["finish_time"]
    lpu_id = data["appointment"]["lpu_id"]
    code = data["appointment"]["code"]
    available_resource_id = data["appointment"]["available_resource_id"]
    complex_resource_id = data["appointment"]["complex_resource_id"]
    priority = data["appointment"].get("priority", 0)

    flag_exist = await people_repository.check(oms_number, birth_date)
    if not flag_exist:
        # hidden creation person
        people_repository.add(oms_number, birth_date)

    await repo.add(oms_number, birth_date, start_time, finish_time, lpu_id, code, available_resource_id, complex_resource_id, priority)
    return web.Response(text="Appointment is create", staus=201)


async def update(request):
    data = await request.json()
    appointment_id = int(request.match_info["appointment_id"])

    oms_number = data["person"]["oms_number"]
    birth_date = data["person"]["birth_date"]

    start_time = data["appointment"]["start_time"]
    finish_time = data["appointment"]["finish_time"]
    priority = data["appointment"].get("priority", 0)

    try:
        await repo.update(oms_number, birth_date, appointment_id, start_time, finish_time, priority)
    except:
        return web.Response(text="Appointment not found", status=404)
    else:
        return web.Response(text="Appointment update")


async def delete(request):
    oms_number = request.query["oms_number"]
    birth_date = request.query["birth_date"]
    appointment_id = request.match_info["appointment_id"]

    try:
        await repo.delete(oms_number, birth_date, appointment_id)
    except:
        return web.Response(text="Person not found", status=404)
    else:
        return web.Response(text=f"Appointment {appointment_id} deleted")
