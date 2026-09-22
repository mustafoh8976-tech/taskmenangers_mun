from dotenv import load_dotenv
import psycopg2
import os


load_dotenv()
password = os.getenv("password_db")


def connect_db():
    try:
        conn = psycopg2.connect(
        user="postgres",
        password=password,
        host="localhost",
        port=5432,
        dbname="hom-tg1",
        )
        return conn
    except Exception as err:
        print("Error конетк не получаеться", err)
        return None


def create_table():
    conn = connect_db()
    if not conn:
        return

    try:
        cur = conn.cursor()
        cur.execute(
            """
            create table if not exists users(
            id serial primary key,
            username varchar(100) not null,
            email varchar(100) not null,
            password varchar(100) check(length(password) > 8)
            );
            """
        )
        cur.execute(
            """
            create table if not exists tasks(
            id serial primary key,
            user_id int references users(id),
            title varchar(200) not null,
            description text,
            due_date timestamp,
            is_completed bool default false,
            created_at timestamp default current_timestamp
            );
            """
        )
        conn.commit()
        print("таблицы созданы")
    except Exception as err:
        conn.rollback()
        print("Error таблицы не создаються", err)
    finally:
        conn.close()
