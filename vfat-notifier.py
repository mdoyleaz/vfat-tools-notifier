### Ns are getting removed from names


import re
import requests
import sqlite3

NETWORKS = ["bsc", "polygon"]

def create_db_connection(db_file):
    return sqlite3.connect(db_file)

def write_to_db(conn, rows):
    cur = conn.cursor()

    for row in rows:
        columns = ', '.join(row.keys())
        placeholders = ', '.join('?' * len(row))

        sql = 'INSERT INTO farms ({}) VALUES ({})'.format(columns, placeholders)

        values = [int(x) if isinstance(x, bool) else x for x in row.values()]
        cur.execute(sql, values)
        
    conn.commit()

def get_file(network):
    url = 'https://raw.githubusercontent.com/vfat-tools/vfat-tools/master/src/static/js/{}.js'.format(network)

    req = requests.get(url)
    return req.content.decode('utf-8')

def parse_js(file, network):
    rows = re.sub(r"[\s\n\t']*", "", file)
    row_search = re.search(r"rows:(.*)]", rows)
    row_list = re.split(r"\[(.*?)\]", row_search.group(0)[7::])

    parsed_rows = []
    for row in row_list:
        split_row = row.split(",")
        if len(split_row) > 2:
            parsed_rows.append({"name": split_row[0], "url": split_row[3], "network": network })

    return parsed_rows

def main():
    file = get_file("polygon")
    rows = parse_js(file, "polygon")

    conn = create_db_connection('vfat_services.db')
    write_to_db(conn, rows)

if __name__ == "__main__":
    main()