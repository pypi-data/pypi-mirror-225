from db_lonewolpy.db import Database

db = Database

def test():
    result = db.execute_query("SELECT * FROM nodes limit 5")
    db.close()
    # print(result)
    for res in result:
        print(res)