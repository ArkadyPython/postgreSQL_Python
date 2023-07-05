import psycopg2
from pprint import pprint


def create_db(cur):
    cur.execute('CREATE TABLE IF NOT EXISTS clients('
                'id SERIAL PRIMARY KEY,'
                'first_name VARCHAR(40) UNIQUE,'
                'last_name VARCHAR(40) UNIQUE,'
                'email VARCHAR(40) UNIQUE'
                ');')
    cur.execute('CREATE TABLE IF NOT EXISTS telephones('
                'client_id INTEGER REFERENCES clients(id),'
                'phone VARCHAR(40) UNIQUE'
                ');')
    return
def add_client(cur, first_name, last_name, email, phone=None):
    cur.execute('INSERT INTO clients (first_name, last_name, email)'
                'VALUES (%s, %s, %s);',
                (first_name, last_name, email))
    cur.execute('SELECT id FROM clients')
    id = cur.fetchone()[0]
    return id
def add_phone(cur, client_id, phone):
    cur.execute('INSERT INTO telephones (client_id, phone)'
                'VALUES (%s, %s);',
                (client_id, phone))
    return client_id
def change_client(cur, id, first_name=None, last_name=None, email=None, phone=None):
    cur.execute(''
                'SElECT * FROM clients '
                'WHERE id = %s'
                , (id, ))
    info = cur.fetchone()
    if first_name is None:
        first_name = info[1]
    if last_name is None:
        last_name = info[2]
    if email is None:
        email = info[3]
    cur.execute(''
                'SELECT * FROM telephones '
                'WHERE client_id = %s'
                , (id, ))
    info1 = cur.fetchone()
    if phone is None:
        phone = info1[1]
    cur.execute('UPDATE clients '
                'SET first_name = %s,'
                'last_name = %s,'
                'email = %s'
                'where id = %s;', (first_name, last_name, email, id))
    cur.execute(''
                'UPDATE telephones SET phone = %s WHERE client_id = %s;'
                , (phone, id, ))
    return id
def delete_client(cur, id):
    cur.execute('DELETE FROM telephones WHERE client_id = %s', (id, ))
    cur.execute('DELETE FROM clients WHERE id = %s', (id, ))
    return id
def delete_phone(cur, client_id):
    cur.execute('DELETE FROM telephones '
                'WHERE client_id = %s', (client_id, ))
    return client_id
def find_client(cur, first_name=None, last_name=None, email=None, phone=None):
    cur.execute("""
                SELECT c.id, c.first_name, c.last_name, c.email, t.phone FROM clients c
                LEFT JOIN telephones t ON c.id = t.client_id
                WHERE c.first_name LIKE %s OR c.last_name LIKE %s
                OR c.email LIKE %s OR t.phone LIKE %s
                """, (first_name, last_name, email, phone))
    return cur.fetchall()
def delete_db(cur):
    cur.execute("""
            DROP TABLE clients, telephones CASCADE;
            """)


with psycopg2.connect(database="clients_db", user="postgres", password="arkadysql") as conn:
    with conn.cursor() as cur:
        delete_db(cur)
        create_db(cur)
        print("БД создана")
        print("Добавлен клиент id: ",
              add_client(cur, "Аркадий", "Подколзин", "arkadyPython@yandex.ru"))
        print("Добавлен клиент id: ",
              add_client(cur, "Анастасия", "Бирюкова", "Anastasia@yandex.ru"))
        cur.execute("""
                        SELECT c.id, c.first_name, c.last_name, c.email, t.phone FROM clients c
                        LEFT JOIN telephones t ON c.id = t.client_id
                        ORDER by c.id
                        """)
        pprint(cur.fetchall())
        print('----------------------')
        print("Телефон добавлен клиенту id: ",
              add_phone(cur, 1, 79237820002))
        print("Телефон добавлен клиенту id: ",
              add_phone(cur, 2, 88005553535))
        cur.execute("""
                                SELECT c.id, c.first_name, c.last_name, c.email, t.phone FROM clients c
                                LEFT JOIN telephones t ON c.id = t.client_id
                                ORDER by c.id
                                """)
        pprint(cur.fetchall())
        print('----------------------')
        print("Изменены данные клиента id: ",
              change_client(cur, 1, "Аркадий", None, '123@outlook.com'))
        cur.execute("""
                                        SELECT c.id, c.first_name, c.last_name, c.email, t.phone FROM clients c
                                        LEFT JOIN telephones t ON c.id = t.client_id
                                        ORDER by c.id
                                        """)
        pprint(cur.fetchall())
        print('----------------------')
        print('Удалили клиента с id: ',
              delete_client(cur, 1))
        cur.execute("""
                                                SELECT c.id, c.first_name, c.last_name, c.email, t.phone FROM clients c
                                                LEFT JOIN telephones t ON c.id = t.client_id
                                                ORDER by c.id
                                                """)
        pprint(cur.fetchall())
        print('----------------------')
        print('Удалили телефон у клиента с id: ',
              delete_phone(cur, 2))
        cur.execute("""
                                                        SELECT c.id, c.first_name, c.last_name, c.email, t.phone FROM clients c
                                                        LEFT JOIN telephones t ON c.id = t.client_id
                                                        ORDER by c.id
                                                        """)
        pprint(cur.fetchall())
        print('----------------------')
        print('Найден клиент : ',
              (find_client(cur, "Анастасия", "Бирюкова", "Anastasia@yandex.ru")))
        print('----------------------')
conn.close()