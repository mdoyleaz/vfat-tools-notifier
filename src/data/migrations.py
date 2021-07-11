from src.data.database import Database

def migrate():
    try:
        db = Database()
        conn = db.connect()
        cur = conn.cursor()

        cur.execute(farms())
        cur.execute(recipients())

        conn.commit()
        conn.close()

        print('Migrations Complete')

        return True
    except Exception as e:
        print('Migration Failed: {}'.format(e))

        return False

def farms():
    return '''
        CREATE TABLE if not exists farms(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        url TEXT NOT NULL,
        network TEXT NOT NULL,
        inserted_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        '''

def recipients():
    return '''
        CREATE TABLE if not exists recipients(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        inserted_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        '''