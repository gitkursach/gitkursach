import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


try:
    # Подключение к существующей базе данных
    connection = psycopg2.connect(user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="123",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="BOT")

    # Курсор для выполнения операций с базой данных
    cursor = connection.cursor()
    # Распечатать сведения о PostgreSQL
    print("Информация о сервере PostgreSQL")
    print(connection.get_dsn_parameters(), "\n")
    # Выполнение SQL-запроса
    cursor.execute("SELECT \"ServiceDate\" FROM \"Server\";")
    # Получить результат
    record = cursor.fetchall()
    print("Вы подключены к - ", record, "\n")
    text = ("text")
    phone = ("phone")
    date = ("10.11.2020")
    cursor.execute(f"INSERT INTO \"USER\"  ( \"date\") VALUES( '{date}');")
    connection.commit()

    cursor.execute(f"INSERT INTO \"USER\"  ( \"date\") VALUES( '{date}');")
    connection.commit()

    #cursor.execute(insert_query, text)

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")


        def postgre():
            try:
                # Подключение к существующей базе данных
                connection = psycopg2.connect(user="postgres",
                                              # пароль, который указали при установке PostgreSQL
                                              password="123",
                                              host="127.0.0.1",
                                              port="5432",
                                              database="BOT")

                # Курсор для выполнения операций с базой данных
                cursor = connection.cursor()
                # Распечатать сведения о PostgreSQL
                print("Информация о сервере PostgreSQL")
                print(connection.get_dsn_parameters(), "\n")
                # Выполнение SQL-запроса
                cursor.execute(
                    f"UPDATE \"PersonalData\" SET \"Phone\" = {message.text} WHERE user_id = {message.from_user.id}")
                connection.commit()

            except (Exception, Error) as error:
                print("Ошибка при работе с PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("Соединение с PostgreSQL закрыто")