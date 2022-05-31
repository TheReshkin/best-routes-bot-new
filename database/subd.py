from main import conn, cursor


def db_table_val(user_id: int, mail: str, password: str, token: str):
    cursor.execute('INSERT INTO user_database (user_id, mail, password, token) VALUES (?, ?, ?, ?)',
                   (user_id, mail, password, token))
    conn.commit()


def db_table_chat_id(user_id: int):
    cursor.execute('INSERT INTO user_database (user_id) VALUES (?)',
                   (user_id))
    conn.commit()
