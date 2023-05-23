import sqlite3 as sq3
from random import randint


class Database_helper():
    """
    Generates all User-Databases
    and is used to manipulate
    """
    def __init__(self, path_2_db: str) -> None:
        self.__db = sq3.connect(database=path_2_db)
        self.__curs = self.__db.cursor()
        # Max Trys for loops
        self.__trys = 0
        self.__tokenlength = 16

        self.__curs.execute("""
                    SELECT count(name)
                    FROM sqlite_master
                    WHERE type='table'
                    AND name='USER'
                    """)

        if self.__curs.fetchone()[0] == 1:
            print("Table USER exists")
        else:
            self.__curs.execute("""
                    CREATE TABLE USER
                    (ID char(10) PRIMARY KEY NOT NULL,
                    FIRSTNAME CHAR(20) NOT NULL,
                    NAME CHAR(20) NOT NULL,
                    EMAIL CHAR(25) NOT NULL
                    );""")
            print("Table USER Created!")

        self.__db.commit()

    def add_user(self, data: list, max_trys=10) -> None:
        sql_statement = """
                        INSERT INTO USER
                        (ID,
                        FIRSTNAME,
                        NAME,
                        EMAIL
                        )
                        VALUES(?,?,?,?)
                        """

        if len(data) > 8:
            print("Too much data given!")
            return

        while True:
            id = ''.join(["{}".format(
                randint(0, 9)) for num in range(0, self.__tokenlength)])

            self.__curs.execute(f"""
                        SELECT count(ID)
                        FROM USER
                        WHERE ID='{id}'
                        """)

            if self.__trys > max_trys:
                print(
                    'Generating User ID failed. Abort adding User. No valid id has been found!')
                return
            elif self.__curs.fetchone()[0] == 1:
                print(f"ID: {id} already exists, generating new one!")
                self.__trys += 1
            else:
                break

        print(f"Adding new User with ID {id}")
        data.insert(0, id)
        self.__curs.execute(sql_statement, data)
        self.__db.commit()


if __name__ == "__main__":
    db_test = Database_helper('Data/test.db')
    inp = ['test', 'Test12', 'h@b.de']
    db_test.add_user(inp)
