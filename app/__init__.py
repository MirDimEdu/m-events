from fastapi import FastAPI

from . import db
from .router import router
from .config import cfg
from .m_utils import YamlConfigManager
from .errors import exception_handlers


app = FastAPI(exception_handlers=exception_handlers)

app.include_router(router)

ConfigManager = YamlConfigManager(interval=30)


@app.on_event('startup')
async def startup():
    await ConfigManager.start()

    await db._database.connect()
    if cfg.STARTUP_DB_ACTION:
        db.create_tables()


@app.on_event('shutdown')
async def shutdown():
    await db._database.disconnect()
