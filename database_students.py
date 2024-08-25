import sqlite3


#1. Создать таблицу countries (страны) c колонками id первичный ключ автоинкрементируемый и колонка title с текстовым не пустым названием страны.
sql_to_create_countries_table = '''
CREATE TABLE countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_title TEXT NOT NULL
)
'''

#3. Добавить таблицу cities (города) c колонками id первичный ключ автоинкрементируемый, колонка title с текстовым не пустым названием города и колонка area площадь города не целочисленного типа данных со значением по умолчанием 0, а также колонка country_id с внешним ключом на таблицу countries.

sql_to_create_cities_table = '''
CREATE TABLE cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    area FLOAT DEFAULT 0,
    country_id INTEGER,
    FOREIGN KEY (country_id) REFERENCES countries(id)
)
'''


sql_to_create_students_table = '''
CREATE TABLE students (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   first_name TEXT NOT NULL,
   last_name TEXT NOT NULL,
   city_id INTEGER,
   FOREIGN KEY (city_id) REFERENCES cities(id)
)
'''


def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        print('Database connection is established!')
    except sqlite3.Error as e:
        print(f'Error connecting to database: {e}')
    return connection

def create_table(connection, sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        # print(f'Table is created with SQL: {sql}')
    except sqlite3.Error as error:
        print(f'Error creating table: {error}')


def insert_data(connection, sql, data):
    try:
        cursor = connection.cursor()
        cursor.executemany(sql, data)
        connection.commit()
        # print(f'Data inserted with SQL: {sql}')
        # print(f'Inserted data: {data}')
    except sqlite3.Error as error:
        print(f' Error inserting data: {error}')

def clear_data(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('DROP TABLE IF EXISTS students')
        cursor.execute('DROP TABLE IF EXISTS cities')
        cursor.execute('DROP TABLE IF EXISTS countries')
        connection.commit()
        print('All data cleared from tables.')
    except sqlite3.Error as e:
        print(f' Error clearing data: {e}')


def get_cities(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, title FROM cities")
        cities = cursor.fetchall()
        print(f'Retrieved cities: {cities}')
        return cities
    except sqlite3.Error as e:
        print(f' Error retrieving cities: {e}')
        return []

def get_students_by_city_id(connection, city_id):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT students.first_name, students.last_name, cities.title, countries.country_title, cities.area
            FROM students
            JOIN cities ON students.city_id = cities.id
            JOIN countries ON cities.country_id = countries.id
            WHERE cities.id = ? 
        """, (city_id,))
        students = cursor.fetchall()
        print(f'Retreived students for city ID {city_id}: {students}')
        return students
    except sqlite3.Error as e:
        print(f' Error retrieving students: {e}')
        return []

def main():
    database = "location.db"
    my_connection = create_connection(database)

    if my_connection is not None:
        print('Successfully connected to database')

        clear_data(my_connection)

        # create tables

        create_table(my_connection, sql_to_create_countries_table)
        create_table(my_connection, sql_to_create_cities_table)
        create_table(my_connection, sql_to_create_students_table)


# 2 counties_data

    countries_data = [
        ('Kyrgyzstan',),
        ('Germany',),
        ('China',),
    ]

    insert_countries_sql = "INSERT INTO countries (country_title) VALUES (?)"
    insert_data(my_connection, insert_countries_sql, countries_data)


# 4 cities_data

    cities_data = [
        ('Bishkek', 127.3, 1),
        ('Osh', 182.5, 1),
        ('Berlin', 891.8, 2),
        ('Beijing', 16410.5, 3),
        ('Shanghai', 6340.5, 3),
        ('Munich', 310.7, 2),
        ('Chengdu', 14378, 3)
    ]
    insert_cities_sql = "INSERT INTO cities (title, area, country_id) VALUES (?, ?, ?)"
    insert_data(my_connection, insert_cities_sql, cities_data)


# 6 students_data

    students_data = [
        ('Jim', 'Chan', 3),
        ('Tina', 'Tan', 7),
        ('Suna', 'Li', 7),
        ('Suzi', 'Wei', 3),
        ('Karl', 'Fischer', 3),
        ('Aidar', 'Bekov', 1),
        ('Alina', 'Kalikova', 2),
        ('Aijan', 'Karimbekova', 1),
        ('Nur', 'Asanov', 2),
        ('Emma', 'Becker', 6),
        ('Oliver', 'Muller', 6),
        ('Maria', 'Schmidt', 3),
        ('Wang', 'Ming', 5),
        ('Sanjar', 'Sultanov', 1),
        ('Jane', 'Smith', 3)
    ]

    insert_students_sql = "INSERT INTO students (first_name, last_name, city_id) VALUES (?, ?, ?)"
    insert_data(my_connection, insert_students_sql, students_data)

    print('Data inserted successfully!')

    while True:
        cities = get_cities(my_connection)
        if not cities:
            print("No cities were found. Try again.")
            break

        print("Вы можете отобразить список учеников по выбранному id города из перечня городов ниже, для выхода из программы введите 0:")
        for city in cities:
            print(f'{city[0]}. {city[1]}')

        city_id = input('Введите id города: ')

        if city_id.isdigit():
            city_id = int(city_id)
            if city_id == 0:
                print("Выход из программы")
                break

            students = get_students_by_city_id(my_connection, city_id)
            if students:
                for student in students:
                    print(f"Имя: {student[0]}, Фамилия: {student[1]}, Город: {student[2]}, Страна: {student[3]}, Площадь города: {student[4]}")
            else:
                print('Ученик в этом городе не найден.')
        else:
            print('Пожалуйста, введите допустимый ID города')

    my_connection.close()



if __name__ == '__main__':
    main()