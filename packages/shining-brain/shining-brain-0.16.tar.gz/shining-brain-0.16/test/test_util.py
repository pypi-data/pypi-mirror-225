import pandas as pd
from shining_brain.util import generate_ddl, generate_column_mapping


def test_generate_ddl_from_csv():
    data_frame = pd.DataFrame({
        'Name': ['Alice'],
        'Start Date': ['2020-02-02'],
        'Age': [18],
        'Salary': [5000.50],
    })
    data_frame.to_csv('./test_data.csv', index=False)

    expected_ddl = (
        "create table table_001 (\n"
        "    id bigint auto_increment primary key,\n"
        "    name varchar(50),\n"
        "    start_date varchar(50),\n"
        "    age int,\n"
        "    salary decimal(16,6),\n"
        "    created datetime default current_timestamp () not null,\n"
        "    updated datetime default current_timestamp () not null\n"
        ");"
    )

    filename = './test_data.csv'
    assert generate_ddl(filename, 'table_001') == expected_ddl


def test_generate_ddl_from_xlsx():
    data_frame = pd.DataFrame({
        'Name': ['Alice'],
        'Start Date': ['2020-02-02'],
        'Age': [18],
        'Salary': [5000.50],
    })
    data_frame.to_excel('./test_data.xlsx', index=False)

    expected_ddl = (
        "create table table_001 (\n"
        "    id bigint auto_increment primary key,\n"
        "    name varchar(50),\n"
        "    start_date varchar(50),\n"
        "    age int,\n"
        "    salary decimal(16,6),\n"
        "    created datetime default current_timestamp () not null,\n"
        "    updated datetime default current_timestamp () not null\n"
        ");"
    )

    filename = './test_data.xlsx'
    assert generate_ddl(filename, 'table_001') == expected_ddl


def test_generate_column_mapping():
    data_frame = pd.DataFrame({
        'Name': ['Alice'],
        'Start Date': ['2020-02-02'],
        'Age': [18],
        'Salary': [5000.50],
    })
    data_frame.to_excel('./test_data.xlsx', index=False)

    expected_column_mapping = {
        'Name': 'name',
        'Start Date': 'start_date',
        'Age': 'age',
        'Salary': 'salary'
    }

    filename = './test_data.xlsx'
    assert generate_column_mapping(filename) == expected_column_mapping
