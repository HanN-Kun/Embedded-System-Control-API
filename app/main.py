from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import user, embedded_system, component, sensor, sensor_reading, device_status,queries,auth,locale,user_role
import logging
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from app.config import settings
from app.core.logging_config import setup_logging
from app.core.exception_handlers import global_exception_handler
from app.core.sentry_setup import init_sentry

setup_logging()

init_sentry([StarletteIntegration(), FastApiIntegration()])

app = FastAPI(title="Embedded System Monitoring API")
app.add_exception_handler(Exception, global_exception_handler)
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

