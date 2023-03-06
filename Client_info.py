import psycopg2


def owerwrite_tables(cur):
        cur.execute ("""
            DROP TABLE IF EXISTS client_phone;
            DROP TABLE IF EXISTS client_info;""")
        return 'OK'
    

def create_bd(cur):
        cur.execute("""CREATE TABLE IF NOT EXISTS client_info (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(40) NOT NULL,
                    last_name VARCHAR(60) NOT NULL,
                    email VARCHAR(60) UNIQUE NOT NULL);""")
                
        cur.execute("""CREATE TABLE IF NOT EXISTS client_phone (
                    id SERIAL PRIMARY KEY,
                    client_id INTEGER NOT NULL REFERENCES client_info(id),
                    phone BIGINT );""")
        return "Выполнено!"
    


# def add_client(first_name,last_name,email):
#     cur.execute("""INSERT INTO client_info(first_name,last_name,email)
#                     VALUES (%s,%s,%s)
#                     RETURNING id;""", (first_name,last_name,email))
#     client_id=cur.fetchone()
#     phone=int(input('Введите номер телефона:'))
#     cur.execute("""INSERT INTO client_phone(client_id,phone) 
#         VALUES(%s,%s) RETURNING id,client_phone.id, phone;""", (client_id,phone))
#     return f'Данные о клиенте  {first_name} {last_name} успешно добавлены'

def add_client(cur,first_name,last_name,email,phone=None):
        cur.execute("""INSERT INTO client_info(first_name,last_name,email)
                    VALUES (%s,%s,%s)
                    RETURNING id;""", (first_name,last_name,email))
        client_id=cur.fetchone()
        if phone!= None:
            cur.execute("""INSERT INTO client_phone(client_id,phone) 
            VALUES(%s,%s) RETURNING id,client_phone.id, phone;""", (client_id,phone))
            return f'Данные о клиенте  {first_name} {last_name} успешно добавлены'
        if phone==None:
            return f'Данные о клиенте  {first_name} {last_name} успешно добавлены, номер телефона не был добавлен'
        

# def add_phone():
#     client_id=int(input('Введите идентификатор клиента:')) 
#     phone=int(input('Введите номер телефона:'))
#     cur.execute("""INSERT INTO client_phone(client_id,phone)
#         VALUES(%s,%s) RETURNING id,client_phone.client_id, phone;""",(client_id,phone))     
#     return f'Номер телефона {phone} для клиента с идентификатором {client_id} успешно добавлен', cur.fetchone() 

def add_phone(cur,client_id, phone):
        cur.execute("""INSERT INTO client_phone(client_id, phone)
            VALUES (%s, %s);
            """, (client_id, phone))
        return ( f'Номер телефона {phone} добавлен для клиента с id: {client_id} ')




def update_client_info(id,first_name=None, last_name=None,email=None,phone=None):
        if first_name!=None:
            cur.execute("""UPDATE client_info SET first_name=%s   
                WHERE id=%s RETURNING id,first_name,last_name;""", (first_name, id))
            print(cur.fetchall())
        if last_name!=None:
            cur.execute("""UPDATE client_info SET last_name=%s   
                WHERE id=%s RETURNING id,first_name,last_name;""", (last_name, id))
            print(cur.fetchall())
        if email!=None:
            cur.execute("""UPDATE client_info SET email=%s   
                WHERE id=%s RETURNING id,first_name,last_name,email;""", (email, id))
            print(cur.fetchall())
        if phone!=None:
            cur.execute("""DELETE FROM client_phone  WHERE client_id=%s;""", (id,))
            cur.execute("""INSERT INTO client_phone VALUES (default, %s, %s)
                    RETURNING client_id, phone; """, (id, phone))
            print(cur.fetchall())
           
    

def delete_phone(cur,client_id,phone):
        cur.execute("""DELETE FROM client_phone WHERE client_id=%s and phone=%s;""",(client_id,phone))
        cur.execute("""SELECT * FROM client_phone WHERE client_id=%s;""",(client_id,))
        print(cur.fetchone())
        return f'Номер телефона {phone} у пользователя с идентификатором {client_id} успешно удален'



def delete_client_info(cur,id:int):
        cur.execute("""DELETE FROM client_phone WHERE client_id=%s ;""",(id,)) 
        cur.execute("""DELETE FROM client_info WHERE id=%s;""",(id,))
        return f'Данные о клиенте с идентификатором {id} успешно удалены'


def find_client_info(cur,first_name=None, last_name=None, email=None, phone=None):     
        if first_name!=None:
            cur.execute("""SELECT * FROM client_info
            WHERE first_name=%s;""", (first_name,))
            print(cur.fetchall())
        if last_name!=None:
            cur.execute("""SELECT * FROM client_info
            WHERE last_name=%s;""",(last_name,))
            print(cur.fetchall())
        if email!=None:
            cur.execute("""SELECT * FROM client_info
            WHERE email=%s;""",(email,))
            print(cur.fetchall())
        if phone!=None:
            cur.execute("""SELECT client_info.id, first_name, last_name, email FROM client_phone 
            JOIN client_info ON client_phone.client_id = client_info.id 
                WHERE phone=%s;""", (phone,))
            print(cur.fetchall())
        else: 
            return('Проверьте правильность введенных данных')


if __name__ == "__main__":
    with psycopg2.connect(database='client_info_db',user='postgres',password='111') as conn:
        with conn.cursor() as cur:
    
            owerwrite_tables(cur)
            print(create_bd(cur)) 
            print(add_client(cur,'Ivan','Ivanov','ivanov@gmail.com','123'))
            print(add_client(cur,'Petr','Petrov','petrov@gmail.com'))
            print(add_client(cur,'Vladimir','Sidorov','sidorov@gmail.com'))
            print(add_phone(cur,1,12345765))
            update_client_info(id=1,phone=934)
            print(delete_phone(cur,1,123))
            print(delete_client_info(cur,1))
            find_client_info(cur,first_name='Petr')


conn.close()



