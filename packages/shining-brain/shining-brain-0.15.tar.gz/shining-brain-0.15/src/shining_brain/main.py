from shining_brain.util import load_file_into_database, generate_ddl, generate_column_mapping
from shining_brain.logger_setup import setup_logger

logger = setup_logger('main.py')


if __name__ == '__main__':
    FILENAME = "/Users/thomas/Documents/english-language/wordbank.csv"
    TABLE_NAME = 'wordbank'
    logger.info(generate_ddl(FILENAME, TABLE_NAME))
    column_mapping = generate_column_mapping(FILENAME)
    load_file_into_database(FILENAME, TABLE_NAME, column_mapping)
