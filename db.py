import json
import os


def get_db():
    if "db.json" not in os.listdir():
        with open("./db.json", "w") as fp:
            fp.write("{}")
    with open("./db.json", "r") as fp:
        return json.load(fp)


def add_file_record(uuid, filename):
    db = get_db()
    db[uuid] = filename
    with open("./db.json", "w") as fp:
        json.dump(db, fp)
