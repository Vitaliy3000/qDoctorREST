import os
import asyncio
from aiohttp import web
from aiohttp_swagger import setup_swagger
import aiohttp_cors
import people
import appointments


app = web.Application()

app.router.add_route("POST", "/people", people.create)
app.router.add_route("GET", "/people/appointments", appointments.read)
app.router.add_route("POST", "/people/appointments", appointments.create)
app.router.add_route("PUT", "/people/appointments/{appointmentId}", appointments.update)
app.router.add_route(
    "DELETE", "/people/appointments/{appointmentId}", appointments.delete
)

cors = aiohttp_cors.setup(
    app,
    defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True, expose_headers="*", allow_headers="*",
        )
    },
)

for route in list(app.router.routes()):
    cors.add(route)

setup_swagger(app, swagger_url="/ui", ui_version=2, swagger_from_file="swagger.yaml")
