from connect_db import connect_db, create_table


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
            conn.commit()
            print(f"Пользователь {user_id} создан автоматически")
    except Exception as err:
        print("Ошибка при создании пользователя:", err)
    finally:
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


def update_task():
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
            "update tasks set title = %s where id = %s;",
            (new_title, task_id),
        )
        conn.commit()
        print("Задача обновлена")
    except Exception as err:
        conn.rollback()
        print("Ошибка:", err)
    finally:
        conn.close()


def delete_task():
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
        cur.execute("delete from tasks where id = %s;", (task_id,))
        conn.commit()
        print("Задача удалена")
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


def main():
    create_table()

    print("\n--- ТАСК МЕНЕДЖЕР ---")

    while True:
        user_id = input("Твой ID: ").strip()
        if not user_id:
            print("ID не может быть пустым")
            continue
        try:
            user_id = int(user_id)
            break
        except ValueError:
            print("ID должно быть числом")

    while True:
        print("\nЧто хочешь сделать?")
        print("1. Добавить задачу")
        print("2. Изменить задачу")
        print("3. Удалить задачу")
        print("4. Посмотреть задачи")
        print("5. Выход")

        choice = input("Выбор: ").strip()

        match choice:
            case "1":
                add_task(user_id)
            case "2":
                update_task()
            case "3":
                delete_task()
            case "4":
                view_tasks(user_id)
            case "5":
                print("Пока")
                break
            case _:
                print("Неверный выбор")


if __name__ == "__main__":
    main()
