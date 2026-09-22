from connect_db import connect_db, create_table
from servie import *


def main():
    create_table()

    print("\n--- ТАСК МЕНЕДЖЕР ---")

    user_id = login()
    if user_id is None:
        return

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
                update_task(user_id)
            case "3":
                delete_task(user_id)
            case "4":
                view_tasks(user_id)
            case "5":
                print("Пока")
                break
            case _:
                print("Неверный выбор")


if __name__ == "__main__":
    main()
