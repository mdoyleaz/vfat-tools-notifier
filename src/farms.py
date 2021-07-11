from src.data.farm import Farm
from src.data.database import Database


def create_farm(**kwargs):
    result = Farm(**kwargs).create()

    return result


def get_all_farms_by_network(network):
    sql = """
    SELECT * FROM farms
    WHERE network = '{}'
    """.format(
        network
    )

    results = Database("farms").query(sql)

    return results
