import sqlite3 as sq3
from random import randint
from uuid import uuid4


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
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    USERTOKEN CHAR(32) NOT NULL,
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
                    (UID INTEGER NOT NULL,
                    BIRTHDAY DATE,
                    PHONE CHAR(20),
                    FOREIGN KEY(UID) REFERENCES USER(ID)
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
                    (UID INTEGER NOT NULL,
                    IBAN CHAR(22),
                    BIC CHAR(11),
                    FOREIGN KEY(UID) REFERENCES USER(ID)
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
                    (UID INTEGER NOT NULL,
                    CITY_ID INTEGER,
                    STREET CHAR(50),
                    NUMBER INTEGER,
                    POSTALCODE INTEGER,
                    FOREIGN KEY(UID) REFERENCES USER(ID),
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
            token = str(uuid4())

            self.__curs.execute(f"""
                        SELECT count(USERTOKEN)
                        FROM USER
                        WHERE USERTOKEN='{token}'
                        """)

            if self.__loop_trys > max_trys:
                print('''
                Generating User ID failed.
                Abort adding User.
                No valid id has been found!
                ''')
                return
            elif self.__curs.fetchone()[0] == 1:
                print(f"ID: {token} already exists, generating new one!")
                self.__loop_trys += 1
            else:
                break
            
        self.__curs.execute(f"""
                        SELECT count(EMAIL)
                        FROM USER
                        WHERE EMAIL='{data[2]}'
                        """)
        
        if self.__curs.fetchone()[0] == 1:
            print(f"User with the EMAIL: {data[2]} already exists")
            print("No User added")
        else:
            print(f"Adding new User with ID {token}")
            data.insert(0, token)
            self.__curs.execute(sql_statement, data)
            self.__db.commit()

    def complete_user(self, data: dict, token: str) -> str:
        sql_sttmnt_PD = """INSERT Into PRIVATE_DATA"""
        sql_sttmnt_CITY = """INSERT Into CITY"""
        sql_sttmnt_ADDRESS = """INSERT Into ADDRESS"""
        sql_sttmnt_BANK = """INSERT Into BANK"""
        sql_sttmnt_BD = """INSERT Into BANKDATA"""

        # Get UserID based on Token
        self.__curs.execute(f"""
                            SELECT *
                            FROM USER
                            WHERE USERTOKEN='{token}'
                            """)
        data = self.__curs.fetchall()
        if len(data) == 1:
            uid, token, name, fname, email = data[0]
            print(f"""
            The User with the token {token},
            has been found""")
        elif len(data) > 1:
            print("Es wurden mehrer Nutzer mit dem gleichen Token gefunden. Bitte wenden sie sich an ihren Andministrator!")
            return "ERROR"
        else:
            print(f"""
            NO User with the token {token},
            has been found""")
            return "ERROR"
        
        return uid



if __name__ == "__main__":
    db_test = Database_helper('Data/test.db')
    inp = ['test', 'Test12', 'h@c.de']
    # db_test.add_user(inp)
    print(db_test.complete_user([], "b786b4b7-9e4f-47a2-81d1-a815377ec9fe"))
