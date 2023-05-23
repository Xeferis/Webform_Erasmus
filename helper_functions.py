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
        self.__loop_trys = 0
        self.__tokenlength = 16

        # Check and/or create USER Table
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
                    (USERTOKEN CHAR(16) PRIMARY KEY NOT NULL,
                    FIRSTNAME CHAR(20) NOT NULL,
                    NAME CHAR(20) NOT NULL,
                    EMAIL CHAR(25) NOT NULL
                    );""")
            print("Table USER Created!")

        # Check and/or create PRIVATE_DATE Table
        self.__curs.execute("""
                    SELECT count(name)
                    FROM sqlite_master
                    WHERE type='table'
                    AND name='PRIVATE_DATA'
                    """)

        if self.__curs.fetchone()[0] == 1:
            print("Table PRIVATE_DATA exists")
        else:
            self.__curs.execute("""
                    CREATE TABLE PRIVATE_DATA
                    (USERTOKEN CHAR(16) NOT NULL,
                    BIRTHDAY DATE,
                    PHONE CHAR(20),
                    FOREIGN KEY(USERTOKEN) REFERENCES USER(USERTOKEN)
                    );""")
            print("Table PRIVATE_DATA Created!")

        # Check and/or create BANK Table
        self.__curs.execute("""
                    SELECT count(name)
                    FROM sqlite_master
                    WHERE type='table'
                    AND name='BANK'
                    """)

        if self.__curs.fetchone()[0] == 1:
            print("Table BANK exists")
        else:
            self.__curs.execute("""
                    CREATE TABLE BANK
                    (BIC char(11) PRIMARY KEY NOT NULL,
                    NAME CHAR(50)
                    );""")
            print("Table PRIVATE_DATA Created!")

        # Check and/or create BANKDATA Table
        self.__curs.execute("""
                    SELECT count(name)
                    FROM sqlite_master
                    WHERE type='table'
                    AND name='BANKDATA'
                    """)

        if self.__curs.fetchone()[0] == 1:
            print("Table BANKDATA exists")
        else:
            self.__curs.execute("""
                    CREATE TABLE BANKDATA
                    (USERTOKEN CHAR(16) NOT NULL,
                    IBAN CHAR(22),
                    BIC CHAR(11),
                    FOREIGN KEY(USERTOKEN) REFERENCES USER(USERTOKEN)
                    FOREIGN KEY(BIC) REFERENCES BANK(BIC)
                    );""")
            print("Table BANKDATA Created!")

        # Check and/or create CITY Table
        self.__curs.execute("""
                    SELECT count(name)
                    FROM sqlite_master
                    WHERE type='table'
                    AND name='CITY'
                    """)

        if self.__curs.fetchone()[0] == 1:
            print("Table CITY exists")
        else:
            self.__curs.execute("""
                    CREATE TABLE CITY
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    NAME CHAR(22)
                    );""")
            print("Table CITY Created!")

        # Check and/or create ADDRESS Table
        self.__curs.execute("""
                    SELECT count(name)
                    FROM sqlite_master
                    WHERE type='table'
                    AND name='ADDRESS'
                    """)

        if self.__curs.fetchone()[0] == 1:
            print("Table ADDRESS exists")
        else:
            self.__curs.execute("""
                    CREATE TABLE ADDRESS
                    (USERTOKEN CHAR(16),
                    CITY_ID INTEGER,
                    STREET CHAR(50),
                    NUMBER INTEGER,
                    POSTALCODE INTEGER,
                    FOREIGN KEY(USERTOKEN) REFERENCES USER(USERTOKEN),
                    FOREIGN KEY(CITY_ID) REFERENCES CITY(ID)
                    );""")
            print("Table ADDRESS Created!")

        self.__db.commit()

    def add_user(self, data: list, max_trys=10) -> None:
        sql_statement = """
                        INSERT INTO USER
                        (USERTOKEN,
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
                        SELECT count(USERTOKEN)
                        FROM USER
                        WHERE USERTOKEN='{id}'
                        """)

            if self.__loop_trys > max_trys:
                print('''
                Generating User ID failed.
                Abort adding User.
                No valid id has been found!
                ''')
                return
            elif self.__curs.fetchone()[0] == 1:
                print(f"ID: {id} already exists, generating new one!")
                self.__loop_trys += 1
            else:
                break

        print(f"Adding new User with ID {id}")
        data.insert(0, id)
        self.__curs.execute(sql_statement, data)
        self.__db.commit()

    def complete_user(self, data: list) -> str:
        sql_statement = """INSERT Into"""

        self.__curs.execute(f"""
                        SELECT count(ID)
                        FROM User_data
                        WHERE USERTOKEN='{id}'
                        """)

        if self.__curs.fetchone()[0] == 1:
            print(f"""
            The User with the ID {id},
            already exists.""")
        else:
            return data

        self.__curs.execute(sql_statement, data)
        self.__db.commit()
        return data


if __name__ == "__main__":
    db_test = Database_helper('Data/test.db')
    inp = ['test', 'Test12', 'h@b.de']
    db_test.add_user(inp)
