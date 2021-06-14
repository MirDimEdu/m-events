from jose import JWTError, jwt
from fastapi import Request

from .config import cfg


class CurrentUser:
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
