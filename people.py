from config import web
import people_repository as repo


async def check(request):
    oms_number = request.query["oms_number"]
    birth_date = request.query["birth_date"]
    flag_exist = await repo.check(oms_number, birth_date)

    if flag_exist:
        return web.Response(text="Person is exist")
    else:
        return web.Response(text="Person not found", status=404)


async def create(request):
    data = await request.json()
    oms_number = data["oms_number"]
    birth_date = data["birth_date"]
    flag_exist = await repo.check(oms_number, birth_date)

    if flag_exist:
        return web.Response(text="Person is exist")
    else:
        await repo.add(oms_number, birth_date)
        return web.Response(text="Person is create", status=201)
