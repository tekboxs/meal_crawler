import pandas as pd

from MealDataBaseReader import connection_configs
from MealDataBaseReader.data_frame_to_product import data_frame_to_product_list
from MealDataBaseReader.db_connection import connect_sql_server
from product_model import ProductModel


def db_connector() -> list[ProductModel]:
    cursor = connect_sql_server(connection_configs)

    product_query = 'SELECT [Cód prod], [Nome produto] FROM produtos;'

    query_result = [list(item) for item in cursor.execute(product_query).fetchall()]


    columns = ['id', 'description']

    frame = pd.DataFrame(query_result, columns=columns)

    return data_frame_to_product_list(frame)
