import sqlite3
import os
from os import path


def connect_db():
    try:
        conn = sqlite3.connect('songs-book.db')
        cursor = conn.cursor()
    except sqlite3.Error as e:
        print(e)
        return None
    return (conn, cursor)


def create_table():
    conn, cursor = connect_db()
    if conn:
        try:
            cursor.execute("DROP TABLE IF EXISTS songs;")
            cursor.execute("""
                CREATE TABLE songs (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    title TEXT, author TEXT,
                    song_text TEXT
                );
            """)
            conn.commit()
        except sqlite3.Error as e:
            print(e)
    conn.close()


def get_text(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text


def prepare_data(dirpath):

    # data = {}
    data = []
    authors = os.listdir(dirpath)
    count = 0
    for author in authors:
        author_dir = os.path.join(dirpath, author)
        if path.isdir(author_dir):
            songs = os.listdir(author_dir)
            for song in songs:
                count += 1
                text = get_text(os.path.join(author_dir, song))
                row = (count, song[:-4], author, text)
                data.append(row)
    return data


def fill_db():
    conn, cursor = connect_db()
    data = prepare_data('songs')
    if conn:
        try:
            cursor.executemany("INSERT INTO songs VALUES (?, ?, ?, ?)", data)
            conn.commit()
        except sqlite3.Error as e:
            print(e)
    conn.close()


def get_data(text=None):
    conn, cursor = connect_db()

    if conn:
        try:
            if not text:
                res = cursor.execute(
                    "SELECT * FROM songs limit 1000"
                ).fetchall()
            else:
                res = cursor.execute(
                    f"SELECT * FROM songs WHERE title LIKE '{text}%'"
                ).fetchall()
        except sqlite3.Error as e:
            print(e)
            res = None
    conn.close()
    return res


if __name__ == '__main__':
    # create_table()
    # fill_db()
    pass
