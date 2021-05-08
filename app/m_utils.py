import os
import asyncio
import yaml
from jose import JWTError, jwt
from aiofile import async_open
from fastapi import Request

from .config import cfg


class YamlConfigManager:
    def __init__(self, interval):
        self._update_interval = interval
        self._config_file = 'config.yaml'
        #self._update_task = asyncio.ensure_future(self._update_loop())

    async def _update_loop(self):
        while True:
            try:
                await self._update()
            except Exception as e:
                print(f'Failed to update config, see you next time \n{repr(e)}')
            await asyncio.sleep(self._update_interval)

    async def _update(self):
        async with async_open(self._config_file, 'r') as f:
            data = yaml.safe_load(await f.read())
#            td = data['server-conf']['port']
#            print(td)
#            if td:
#                cfg.DB_CONNECTION_STRING = int(td)
#            self._config = models.Config.parse_obj(data)

    async def start(self):
        self._update_task = asyncio.ensure_future(self._update_loop())


class CurrentUser():
    def __init__(self, account_id, role, session_id, client, login_time):
        self.account_id = account_id
        self.role = role
        self.session_id = session_id
        self.login_time = login_time
        self.client = client


async def get_current_user(request: Request):
    token = request.cookies.get(cfg.AUTH_TOKEN_NAME)
    if not token:
        HTTPabort(401, 'Incorrect token name')

    try:
        payload = jwt.decode(token, cfg.TOKEN_SECRET_KEY, algorithms=['HS256'])
        account_id: int = payload.get('account_id')
        role: str = payload.get('role')
        session_id = uuid.UUID(payload.get('session_id'))
        login_time = datetime.fromisoformat(payload.get('login_time'))
        client = payload.get('client')
    except:
        HTTPabort(401, 'Incorrect token data')

    return CurrentUser(account_id, role, session_id, client, login_time)
