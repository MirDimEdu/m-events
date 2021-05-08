import uvicorn
from argparse import ArgumentParser

from app import app
from app.config import cfg


if __name__ == '__main__':
    parser = ArgumentParser(description='Events Management micro-service')
    parser.add_argument('--create-tables',
                        action='store_true',
                        dest='recreate_tables',
                        help='(Re)Creating events database tables before launch.')

    args = parser.parse_args()
    if args.recreate_tables:
        cfg.STARTUP_DB_ACTION = True
    
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config['formatters']['access']['fmt'] = '%(asctime)s - %(client_addr)s - "%(request_line)s" %(status_code)s'

    uvicorn.run(
        'main:app',
        host=cfg.HOST,
        port=cfg.PORT,
        log_config=log_config,
        reload=False
    )
