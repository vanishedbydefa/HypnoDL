import sqlite3 as sl

def connect_db():
    con = sl.connect('id-db.db')
    try:
        with con:
            con.execute("""
                CREATE TABLE IDS (
                    id TEXT,
                    url TEXT,
                    location TEXT,
                    date TEXT,
                    category TEXT
                );
            """)
    except sl.OperationalError:
        print("    -> Database already created")
    else:
        print("    -> Database created")
    return con

def insert_db(con, _id, _url, _location, _date, _category, update_db):
    cursor = con.cursor()
    if update_db:
        sql = 'UPDATE IDS SET location = ?, date = ?, category = ? WHERE id = ?'
        data = (_location, _date, _category, _id)
    else:
        sql = 'INSERT INTO IDS (id, url, location, date, category) values(?, ?, ?, ?, ?);'
        data = (_id, _url, _location, _date, _category)
    cursor.execute(sql, data)
    con.commit()
    cursor.close()

def request_db(con, _id):
    entrys = []
    with con:
        data = con.execute("SELECT * FROM IDS WHERE id ==" + _id)
        for row in data:
            for i in range(len(row)):
                entrys.append(row[i])
    return entrys
