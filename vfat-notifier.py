import re
import requests

from src import farms
import src.data.migrations as migrations


NETWORKS = ["bsc", "polygon"]


def get_file(network):
    url = "https://raw.githubusercontent.com/vfat-tools/vfat-tools/master/src/static/js/{}.js".format(
        network
    )

    req = requests.get(url)
    return req.content.decode("utf-8")


def parse_js(file, network):
    rows = re.sub(r'[\s\n\t\'"]*', "", file)
    row_search = re.search(r"rows:(.*)]", rows)
    row_list = re.split(r"\[(.*?)\]", row_search.group(0)[8::])

    parsed_rows = []
    for row in row_list:
        split_row = row.split(",")
        if len(split_row) > 2:
            parsed_rows.append(
                {"name": split_row[0], "url": split_row[3], "network": network}
            )

    return parsed_rows


def main():
    new_farms = []

    for network in NETWORKS:
        file = get_file(network)
        rows = parse_js(file, network)

        for row in rows:
            if farms.create_farm(**row):
                new_farms.append(row)

    ### Send in notification
    print(new_farms)


if __name__ == "__main__":
    # Run migrations
    migrations.migrate()

    main()
