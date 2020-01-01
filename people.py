from config import web
import people_repository as repo


async def create(request):
    data = await request.json()
    omsNumber = data["omsNumber"]
    birthDate = data["birthDate"]
    flag_exist = await repo.check(omsNumber, birthDate)

    if flag_exist:
        return web.Response(text="Person is exist")
    else:
        await repo.add(omsNumber, birthDate)
        return web.Response(text="Person is create", status=201)
