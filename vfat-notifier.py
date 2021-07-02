### Ns are getting removed from names


import re
import requests
import sqlite3

NETWORKS = ["bsc", "polygon"]

def create_db_connection(db_file):
    return sqlite3.connect(db_file)

def write_to_db(rows):
    conn = sqlite3.connect('vfat_db.db')
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
    return str(req.content)

def parse_js(file, network):
    row_search = re.search(r"rows:(.*)]", file)
    ## Remove all white space, \\n and \\'
    rows = re.sub(r"[\\'\\n]*", "", file[row_search.start()+7:row_search.end()-1])
    ## Splits string lists into python lists
    row_list = re.split(r"\[(.*?)\]", rows)

    parsed_rows = []
    for row in row_list:
        split_row = row.split(",")
        if len(split_row) > 2:
            parsed_rows.append({"name": split_row[0], "url": split_row[3], "network": network })

    return parsed_rows

def main():
    create_db_connection('vfat_services.db')
    file = get_file("polygon")
    rows = parse_js(file, "polygon")
    write_to_db(rows)
if __name__ == "__main__":
    main()