import sqlite3

def connect():
    con = sqlite3.connect('database.db')
    con.row_factory = dict_factory

    return con

# Returns query results as a dictionary, instead of a of a tuple
def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def query(sql):
    con = connect()
    cur = con.cursor()

    cur.execute(sql)

    results = cur.fetchall()

    con.close()

    return results

def insert(table, data):
    try:
        conn = connect()
        cur = conn.cursor()

        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))

        sql = 'INSERT INTO {} ({}) VALUES ({})'.format(table, columns, placeholders)
        values = [int(x) if isinstance(x, bool) else x for x in data.values()]

        cur.execute(sql, values)

        conn.commit()
        conn.close()

    except Exception as e:
        print(e)

    return 

