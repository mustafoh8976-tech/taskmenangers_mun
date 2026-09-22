from connect_db import connect_db
from getpass import getpass


def login():
    email = input("Email: ").strip()
    password = getpass("Пароль: ")
    conn=connect_db()
    if not conn:
        return None

    cur = None
    try:
        cur=conn.cursor()
        cur.execute(
            "select id from users where email = %s and password = %s;",
            (email, password),
        )
        user = cur.fetchone()
        if user is None:
            print("Неверный email или пароль")
            return None

        print("Вход выполнен")
        return user[0]
    except Exception as err:
        print('Ошибка входа:', err)
        return None
    finally:
        if cur is not None:
            cur.close()
        conn.close()


def ensure_user_exists(user_id):
    conn = connect_db()
    if not conn:
        return

    try:
        cur = conn.cursor()
        cur.execute("select id from users where id = %s;", (user_id,))
        if cur.fetchone() is None:
            username = f"user_{user_id}"
            email = f"user{user_id}@mail.com"
            password = f"pass{user_id}word"
            cur.execute(
                "insert into users (id, username, email, password) values (%s, %s, %s, %s);",
                (user_id, username, email, password),
            )
            print(f"Пользователь {user_id} создан автоматически")
    except Exception as err:
        print("Ошибка при создании пользователя:", err)
    finally:
        conn.commit()
        conn.close()


def add_task(user_id):
    ensure_user_exists(user_id)
    title = input("Название задачи: ").strip()
    description = input("Описание: ").strip()

    if not title:
        print("Название не может быть пустым")
        return

    conn = connect_db()
    if not conn:
        return

    try:
        cur = conn.cursor()
        cur.execute(
            "insert into tasks (user_id, title, description) values (%s, %s, %s);",
            (user_id, title, description),
        )
        conn.commit()
        print("Задача добавлена")
    except Exception as err:
        conn.rollback()
        print("Ошибка:", err)
    finally:
        conn.close()


def update_task(user_id):
    try:
        task_id = int(input("ID задачи: "))
    except ValueError:
        print("ID должно быть числом")
        return

    new_title = input("Новое название: ").strip()
    if not new_title:
        print("Название не может быть пустым")
        return

    conn = connect_db()
    if not conn:
        return

    try:
        cur = conn.cursor()
        cur.execute(
            "update tasks set title = %s where id = %s and user_id = %s;",
            (new_title, task_id, user_id),
        )
        conn.commit()
        print("Задача обновлена" if cur.rowcount else "Задача не найдена")
    except Exception as err:
        conn.rollback()
        print("Ошибка:", err)
    finally:
        conn.close()


def delete_task(user_id):
    try:
        task_id = int(input("ID задачи для удаления: "))
    except ValueError:
        print("ID должно быть числом")
        return

    conn = connect_db()
    if not conn:
        return

    try:
        cur = conn.cursor()
        cur.execute(
            "delete from tasks where id = %s and user_id = %s;",
            (task_id, user_id),
        )
        conn.commit()
        print("Задача удалена" if cur.rowcount else "Задача не найдена")
    except Exception as err:
        conn.rollback()
        print("Ошибка:", err)
    finally:
        conn.close()


def view_tasks(user_id):
    conn = connect_db()
    if not conn:
        return

    try:
        cur = conn.cursor()
        cur.execute("select id, title, description from tasks where user_id = %s;", (user_id,))
        tasks = cur.fetchall()

        if not tasks:
            print("Список задач пуст")
            return

        print("\n=-----= СПИСОК ЗАДАЧ =-----=")
        for task in tasks:
            print(f"ID: {task[0]} | Название: {task[1]} | Описание: {task[2]}")
    except Exception as err:
        print("Ошибка:", err)
    finally:
        conn.close()
        
        