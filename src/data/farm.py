from src.data.database import Database


class Farm(Database):
    def __init__(self, **kwargs):
        self.id = id
        self.data = kwargs

        Database.__init__(self, table="farms")

    def create(self):
        sql_query = """
        SELECT * FROM farms 
        WHERE name = '{}' AND network = '{}'
        """.format(
            self.data["name"], self.data["network"]
        )
        if self.query(sql_query):
            # print("\ninsert failed: record already exists - {}".format(self.data))

            return False

        # Appends create method in 'Database' class
        result = super().create()

        return result
