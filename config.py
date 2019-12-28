import os
import asyncio
from aiohttp import web
from aiohttp_swagger import setup_swagger
import people
import appointments


app = web.Application()

app.router.add_route("GET", "/people", people.check)
app.router.add_route("POST", "/people", people.create)
app.router.add_route("GET", "/people/appointments", appointments.read)
app.router.add_route("POST", "/people/appointments", appointments.create)
app.router.add_route("PUT", "/people/appointments/{appointment_id}", appointments.update)
app.router.add_route("DELETE", "/people/appointments/{appointment_id}", appointments.delete)

setup_swagger(app, swagger_url="/ui", ui_version=2, swagger_from_file="swagger.yaml")
