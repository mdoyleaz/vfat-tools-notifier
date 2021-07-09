import src.data.db as db

def get_all_farm_names_by_network(network):
    sql = '''
    SELECT * FROM farms
    WHERE network = '{}'
    '''.format(network)
    results = db.query(sql)

    return results

def create_farm(data):
    sql_query = '''
    SELECT * FROM farms 
    WHERE name = '{}' AND network = '{}'
    '''.format(data['name'], data['network'])
    if not db.query(sql_query):
        db.insert('farms', data)
        return True
       
    return False