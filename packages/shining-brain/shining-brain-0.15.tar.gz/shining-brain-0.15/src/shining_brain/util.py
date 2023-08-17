import re
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
import pandas as pd
import yaml
from shining_brain.logger_setup import setup_logger

logger = setup_logger("util.py")


def load_file_into_database(filename, table_name, column_mapping):
    base = declarative_base()

    with open('db_config.yaml', 'r', encoding='UTF-8') as file:
        db_config = yaml.safe_load(file)

    user = db_config["user"]
    password = db_config["password"]
    host = db_config["host"]
    database = db_config["database"]
    url = f'mysql+mysqlconnector://{user}:{password}@{host}/{database}'
    engine = create_engine(url)
    base.metadata.create_all(engine)

    if filename.endswith('.csv'):
        data_frame = pd.read_csv(filename)
    elif filename.endswith('.xlsx') or filename.endswith('.xls'):
        data_frame = pd.read_excel(filename)
    else:
        logger.warning('Unknown file type')
        return

    data_frame.rename(columns=column_mapping, inplace=True)

    data_frame.to_sql(table_name, con=engine, index=False, if_exists='append')
    logger.info('Data successfully loaded into the database')


def map_dtype(dtype):
    if "int" in str(dtype):
        return "int"
    if "float" in str(dtype):
        return "decimal(16,6)"
    if "datetime" in str(dtype):
        return "datetime"
    return "varchar(50)"


def to_snake_case(title):
    title = title.replace(' ', '')
    title = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', title)
    title = re.sub('([a-z0-9])([A-Z])', r'\1_\2', title)
    return re.sub(r'\W+', '_', title).lower()


def generate_ddl(file_path, table_name="table_name"):
    if file_path.endswith('.csv'):
        data_frame = pd.read_csv(file_path, nrows=1)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        data_frame = pd.read_excel(file_path, nrows=1)
    else:
        logger.warning('Unknown file type')
        return None

    ddl = f"create table {table_name} (\n"
    ddl += "    id bigint auto_increment primary key,\n"
    for column, dtype in data_frame.dtypes.items():
        mysql_type = map_dtype(dtype)
        ddl += f"    {to_snake_case(column)} {mysql_type},\n"

    ddl += "    created datetime default current_timestamp () not null,\n"
    ddl += "    updated datetime default current_timestamp () not null,\n"
    return ddl.rstrip(",\n") + "\n);"


def generate_column_mapping(file_path):
    if file_path.endswith('.csv'):
        data_frame = pd.read_csv(file_path, nrows=1)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        data_frame = pd.read_excel(file_path, nrows=1)
    else:
        logger.warning('Unknown file type')
        return None

    column_mapping = {}
    for column in data_frame.columns:
        column_mapping[column] = to_snake_case(column)

    return column_mapping
