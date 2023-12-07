from faker import Faker
import random

def generate_sql_table(table_name, num_records=10):
    fake = Faker()
    sql_query = f'''
    CREATE TABLE {table_name} (
        id INT PRIMARY KEY,
        product_name VARCHAR(255),
        origin_country VARCHAR(255),
        price DECIMAL(10, 2)
    );
    '''

    for i in range(1, num_records + 1):
        product_name = fake.word()
        origin_country = fake.country()
        while ("'" in origin_country):
            origin_country = fake.country()
        price = round(random.uniform(1, 1000), 2)
        
        sql_query += f'''
        INSERT INTO {table_name} (id, product_name, origin_country, price)
        VALUES ({i}, '{product_name}', '{origin_country}', {price});
        '''

    return sql_query

def save_to_file(sql_code, filename='output.sql'):
    with open(filename, 'w') as file:
        file.write(sql_code)

# Пример использования
table_name = 'products4'
num_records = 5283
sql_code = generate_sql_table(table_name, num_records)
save_to_file(sql_code, 'output4.sql')
