from shining_brain.util import load_file_into_database, generate_ddl, generate_column_mapping
from shining_brain.logger_setup import setup_logger

logger = setup_logger('main.py')


if __name__ == '__main__':
    TRNSACTION= "/Users/thomas/Documents/english-language/transactions.csv"
    logger.info(generate_ddl(TRNSACTION, 'transaction'))
    TABLE_NAME = 'transaction'
    column_mapping= generate_column_mapping(TRNSACTION)
    before_statement = f'delete from {TABLE_NAME} where id > 0'
    after_statement = f'update {TABLE_NAME} set amount = amount * 100 where id > 0'
    load_file_into_database(TRNSACTION, TABLE_NAME, column_mapping, before_statement, after_statement)