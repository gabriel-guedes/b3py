import toml
import logging
import logging.config

db_config = toml.load('db_config.toml')

db_user = db_config['db']['user']
db_password = db_config['db']['password']
db_host = db_config['db']['host']
db_port = db_config['db']['port']
db_schema = db_config['db']['schema']

def get_logger(name='root', level=logging.DEBUG):
    log_config = toml.load('log_config.toml')
    logging.config.dictConfig(log_config)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return(logger)

if __name__ == '__main__':
    pass