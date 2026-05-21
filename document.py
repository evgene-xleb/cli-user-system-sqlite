import sqlite3

# registration and login for terminal

conn = sqlite3.connect("first.db")
comand = conn.cursor()


def create_db(name_db):
    comand.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {name_db}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(250),
            email VARCHAR(250),
            phone TEXT,
            password VARCHAR(30),
            role VARCHAR(10)
        )
    """
    )


def registration():
    name = input("Ваше имя: ")
    email = input("Ваша почта: ")
    phone = input("Ваш номер телефона: ")
    password = input("Придумайте пароль: ")

    shifr_password = ""

    for leter in password:
        if isinstance(leter, int):
            shifr_password += f"{leter} "
        else:
            shifr_password += f"{ord(leter)} "

    comand.execute(
        "INSERT INTO users (name, email, phone, password, role) VALUES (?, ?, ?, ?, ?)",
        (name, email, phone, shifr_password, "user"),
    )
    conn.commit()


def login():
    login_users = input("Почта или номер телефона: ")
    password = input("Ваш пароль: ")
    comand.execute(
        "SELECT email, name, role, password FROM users WHERE email = ? OR phone = ?",
        (login_users, login_users),
    )
    data = comand.fetchone()

    if data is None:
        return False

    correct_password = ""
    for leter in data[3].split():
        correct_password += chr(int(leter))

    if password == correct_password:
        print(
            f"\nВы вошли в аккаунт {data[1]}, ваша роль: {data[2]}. \nПод почтой {data[0]}. \nСпасибо что остаетесь с нами!"
        )
        return (data[0], data[1], data[2])
    else:
        return False


def show_db_info(name_db):
    comand.execute("SELECT * FROM ?", (name_db))
    data = comand.fetchall()
    print(data)


def on_programm():
    login_registration = int(input("1)Войти \n2)Зарегистрироваться\n"))
    if login_registration == 1:
        info_user = login()
        if info_user:
            command = int(
                input(
                    "\nПока вы можете выбрать только 2 команды. \n1)Выйти с аккаунта, \n2)Вывести данные всей базы юзеров, \n3)Выдать роль\n4)Создать базу\n"
                )
            )
            if command == 1:
                print("Вы вышли с аккаунта")
                on_programm()
            elif command == 2:
                if info_user[2] == "admin":
                    name_db = input("Имя бд: ")
                    show_db_info(name_db)
            elif command == 3:
                if info_user[2] == "admin":
                    role = input("Какую роль вы хотите выдать ? ")
                    user_name = input("У кого пользователя ? ")
                    comand.execute(
                        """
                        UPDATE users
                        SET role = ?
                        WHERE email = ? OR phone = ?
                        """,
                        (role, user_name, user_name),
                    )
            elif command == 4:
                name_db = input("Имя базы данных ? ")
                create_db(name_db)
        else:
            print("У вас ошибки при вводе данных")
    elif login_registration == 2:
        registration()
    else:
        print("Данной комманды не существует")


while True:
    on_programm()

conn.close()
