import psycopg2
import random

con = psycopg2.connect(
  database="homework",
  user="postgres",
  password="12345",
  host="127.0.0.1",
  port="5432"
)

print("Database opened successfully")


def create_table():
  cur = con.cursor()
  cur.execute('''CREATE TABLE IF NOT EXISTS CLIENTS  
       (CLIENT_ID INT PRIMARY KEY NOT NULL,
       NAME TEXT,
       SURNAME TEXT,
       EMAIL TEXT,
       PHONE VARCHAR(15));''')

  print("Table created successfully")
  con.commit()


def insert():
  name = input("Введите Имя: ")
  name = f"'{name}'"
  surname = input("Введите Фамилию: ")
  surname = f"'{surname}'"
  email = input("Введите Email: ")
  email = f"'{email}'"
  phone = input("Введите Номер телефона (Enter для пропуска): ")
  if phone == '':
    phone = 'отсутствует'
  phone = f"'{phone}'"
  while (True):
    id = random.randint(0, 100)
    cur = con.cursor()
    cur.execute(f'SELECT EXISTS (SELECT CLIENT_ID FROM CLIENTS WHERE CLIENT_ID = {id}')
    c = cur.fetchall()
    if not c[0][0]:
      break
  cur.execute(
    f'INSERT INTO CLIENTS (CLIENT_ID,NAME,SURNAME,EMAIL,PHONE) VALUES ({id}, {name}, {surname}, {email}, {phone})'
  )

  con.commit()
  print("Record inserted successfully")


def add_phone():
  name = input("Введите Имя существующего клиента: ")
  name = f"'{name}'"
  surname = input("Введите Фамилию существующего клиента: ")
  surname = f"'{surname}'"
  cur = con.cursor()
  cur.execute(f'SELECT EXISTS (SELECT CLIENT_ID FROM CLIENTS WHERE NAME = {name} AND SURNAME = {surname})')
  c_inf = cur.fetchall()
  if c_inf[0][0]:
    cur.execute(f'SELECT CLIENT_ID, EMAIL FROM CLIENTS WHERE NAME = {name} AND SURNAME = {surname}')
    c_email = cur.fetchall()
    phone = input("Введите номер телефона клиента: ")
    phone = f"'{phone}'"
    pr = 'отсутствует'
    pr = f"'{pr}'"
    cur.execute(f'SELECT EXISTS (SELECT CLIENT_ID FROM CLIENTS WHERE NAME = {name} AND SURNAME = {surname} AND PHONE = {pr})')
    b = cur.fetchall()
    if b[0][0]:
      cur.execute(f'SELECT CLIENT_ID, NAME FROM CLIENTS WHERE NAME = {name} AND SURNAME = {surname} AND PHONE = {pr}')
      c_id = cur.fetchall()
      cur.execute(f"UPDATE CLIENTS set PHONE = {phone} where CLIENT_ID = {c_id[0][0]}")
      con.commit()
    else:
      while (True):
        id = random.randint(0, 100)
        cur.execute(f'SELECT EXISTS (SELECT CLIENT_ID FROM CLIENTS WHERE CLIENT_ID = {id})')
        c = cur.fetchall()
        if not c[0][0]:
          break
      p = f"'{c_email[0][1]}'"
      cur.execute(
        f'INSERT INTO CLIENTS (CLIENT_ID,NAME,SURNAME,EMAIL,PHONE) VALUES ({id}, {name}, {surname}, {p}, {phone})'
      )
      con.commit()
  else:
    print("Клиента не существует ")


add_phone()
con.close()