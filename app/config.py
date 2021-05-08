import os
from types import SimpleNamespace


cfg = SimpleNamespace()


def _get_db_connection_string():
    db_connection_string = os.getenv('DB_CONNECTION_STRING')
    if db_connection_string:
        return db_connection_string
    return 'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}'.format(**os.environ)


def _get_m_search_connection_string(MS_HOST, MS_PORT):
    m_search_connection_string = os.getenv('M_SEARCH_CONNECTION_STRING')
    if m_search_connection_string:
        return m_search_connection_string
    return 'http://{MS_HOST}:{MS_PORT}'


cfg.TOKEN_SECRET_KEY = os.getenv('TOKEN_SECRET_KEY', 'X-MIRDIMEDU-KEY')
cfg.AUTH_TOKEN_NAME = os.getenv('AUTH_TOKEN_NAME', 'X-MIRDIMEDU-Token')

cfg.HOST = os.getenv('EVENTS_HOST', '0.0.0.0')
cfg.PORT = int(os.getenv('EVENTS_PORT', '8004'))
cfg.DOMAIN = os.getenv('EVENTS_DOMAIN', 'localhost')

cfg.DB_CONNECTION_STRING = _get_db_connection_string()
cfg.STARTUP_DB_ACTION = False

cfg.MS_HOST = os.getenv('M_SEARCH_HOST', '127.0.0.1')
cfg.MS_PORT = int(os.getenv('M_SEARCH_PORT', '8005'))
cfg.MS_ADDR = _get_m_search_connection_string(cfg.MS_HOST, cfg.MS_PORT)
