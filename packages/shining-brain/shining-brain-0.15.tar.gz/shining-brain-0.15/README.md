# Shining-Brain: Data Analysis Tools

Shining-Brain is a powerful data analysis toolkit designed to streamline the process of working with CSV and Excel files and integrating them with MySQL. With Shining-Brain, you can effortlessly generate Data Definition Language (DDL) from CSV or Excel files and load data from both CSV and Excel files directly into MySQL databases.

## Features

### Generate DDL from CSV or Excel File

With Shining-Brain, you can convert your CSV or Excel files into MySQL Data Definition Lanagues (DDL), allowing you to create database tables that match the structure of your data quickly.

### Generate Column Mapping from CSV or Excel File

You can check the column mapping to decide where to use it or update your original file.

### Load CSV and Excel into MySQL

Shining-Brain simplifies the process of loading data from CSV and Excel files into MySQL. Where you're importing large datasets or working with complex data structures, Shining-Brain handles the process seamlessly.

## Installation

You can install Shinning-Brain using pip3:

``` bash
pip3 install shining-brain
```

## Usage

### Generate DDL from CSV or Excel File

``` python
from shinning-brain.util import generate_ddl

ddl = generate_ddl('your.csv', 'your_table_name')
ddl = generate_ddl('your.xlsx', 'your_table_name')
```

### Generate Column Mapping from CSV or Excel File

```python
from shinning-brain.util import generate_column_mapping

column_mapping = generate_column_mapping('your.csv', 'your_table_name')
column_mapping = generate_column_mapping('your.xlsx', 'your_table_name')
```
### Loading CSV and Excel into MySQL

``` python
from shinning-brain.util import load_file_into_database

filename = "your.csv" # or your.xlsx
column_mapping = {
	'Word': 'word',
	'Search Date': 'search_date',
	'Class': 'class'
}
table_name = 'your_table_name'

load_file_into_database(filename, table_name, column_mapping)
```

## Dependencies

Shining-Brain relies on the following libraries:

- pandas
- sqlalchemy
- pyyaml

## Contributing

We welcome contributions to Shining-Brain! If you have a feature request or bug report or want to contribute code, please open an issue or pull request on our GitHub repository.

## License

Shining-Brain is released under MIT License. See the LICENSE file for more details.

## Contact

For questions or support, please get in touch with the Shinning-Brain team.