from config import web
import repository as repo


async def create(request):
    data = await request.json()
    omsNumber = data["omsNumber"]
    birthDate = data["birthDate"]
    flag_exist = await repo.check_person(omsNumber, birthDate)

    if flag_exist:
        return web.Response(text="Person is exist")
    else:
        await repo.add_person(omsNumber, birthDate)
        return web.Response(text="Person is create", status=201)
