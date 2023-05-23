import sqlite3 as sq3
import random as rnd


class Database_helper():
    def __init__(self, path_2_db: str) -> None:
        _db = sq3.connect(database=path_2_db)
        curs = _db.cursor()
        curs.execute("""
                    SELECT count(name)
                    FROM sqlite_master
                    WHERE type='table'
                    AND name='USER'
                    """)

        if curs.fetchone()[0] == 1:
            print("Table USER exists")
        else:
            curs.execute("""
                    CREATE TABLE USER
                    (ID char(10) PRIMARY KEY NOT NULL,
                    FIRSTNAME CHAR(20) NOT NULL,
                    NAME CHAR(20) NOT NULL,
                    EMAIL CHAR(25) NOT NULL,
                    PHONE CHAR(25) NOT NULL,
                    STREET CHAR(50) NOT NULL,
                    POSTCODE CHAR(6) NOT NULL,
                    CITY CHAR(50) NOT NULL,
                    STATE CHAR(50) NOT NULL
                    );""")
            print("Table USER Created!")

        _db.commit()

    def add_data(self, data: list, max_trys=10):
        if len(data) > 8:
            print("Too much data given!")
            return
        sql_statement = """
                        INSERT INTO USER
                        (ID,
                        FIRSTNAME,
                        NAME,
                        EMAIL,
                        PHONE,
                        STREET,
                        POSTCODE,
                        CITY,
                        STATE)
                        VALUES(?,?,?,?,?,?,?,?,?)
                        """
        curs = self._db.cursor()
        trys = 0
        n = 10
        while True:
            id = ''.join(["{}".format(rnd.randint(0, 9)) for num in range(0, n)])
            curs.execute(f"""
                        SELECT count(ID)
                        FROM USER
                        WHERE ID='{id}'
                        """)
            if trys > max_trys:
                print(
                    'Generating User ID failed. Abort adding User. No valid id has been found!')
                return
            elif curs.fetchone()[0] == 1:
                print(f"ID: {id} already exists, generating new one!")
                trys += 1
            else:
                break
        print(f"Adding new User with ID {id}")
        data.insert(0, id)
        curs.execute(sql_statement, data)
        self._db.commit()


if __name__ == "__main__":
    db_test = Database_helper('test.db')
    inp = ['test', 'Test12', 'h@b.de', '0568432165877',
           'Street', '34281', 'Gudensberg', 'Hessen']
    db_test.add_data(inp)
