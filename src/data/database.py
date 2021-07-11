import sqlite3


class Database(object):
    def __init__(self, table=None):
        self.table = table

    def connect(self):
        con = sqlite3.connect("database.db")
        con.row_factory = self.dict_factory

        return con

    # Returns query results as a dictionary, instead of a of a tuple
    def dict_factory(func, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]

        return d

    def create(self):
        try:
            con = self.connect()
            cur = con.cursor()

            columns = ", ".join(self.data.keys())
            placeholders = ", ".join("?" * len(self.data))

            sql = "INSERT INTO {} ({}) VALUES ({})".format(
                self.table, columns, placeholders
            )
            values = [int(x) if isinstance(x, bool) else x for x in self.data.values()]

            cur.execute(sql, values)
            con.commit()

            con.close()

            print("{} - insert success: {}".format(self.table, self.data))

            return True

        except Exception as e:
            print(
                "{} - insert failed: {} \n error: {}".format(self.table, self.data, e)
            )

        return False

    def delete(self):
        sql = """
        DELETE FROM {} 
        WHERE id = {}
        """.format(
            self.table, self.id
        )
        print(self.id)
        try:
            con = self.connect()
            cur = con.cursor()

            cur.execute(sql)
            con.commit()

            con.close()
        except Exception as e:
            print(e)

            return False

        return True

    def query(self, sql):
        con = self.connect()
        cur = con.cursor()

        cur.execute(sql)
        results = cur.fetchall()

        con.close()

        return results
