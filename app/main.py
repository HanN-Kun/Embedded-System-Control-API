from fastapi import FastAPI
from app.database import Base, engine
from app import models

from app.routers import user, embedded_system, component, sensor, sensor_reading, device_status,queries,auth,locale,user_role



app = FastAPI(title="Embedded System Monitoring API")

app.include_router(user.router)
app.include_router(embedded_system.router)
app.include_router(component.router)
app.include_router(sensor.router)
app.include_router(sensor_reading.router)
app.include_router(device_status.router)
app.include_router(queries.router)
app.include_router(auth.router)
app.include_router(locale.router)    
app.include_router(user_role.router)

