import toml

config = toml.load('config.toml')

db_user = config['db']['user']
db_password = config['db']['password']
db_host = config['db']['host']
db_port = config['db']['port']
db_schema = config['db']['schema']

if __name__ == '__main__':
    pass