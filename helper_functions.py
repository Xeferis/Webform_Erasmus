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
                    (UID INTEGER PRIMARY KEY AUTOINCREMENT,
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
                    (UID INTEGER,
                    BIRTHDAY DATE,
                    PHONE CHAR(20),
                    FOREIGN KEY(UID) REFERENCES USER(UID)
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
                    (UID INTEGER,
                    IBAN CHAR(22),
                    BIC CHAR(11),
                    FOREIGN KEY(UID) REFERENCES USER(UID)
                    FOREIGN KEY(BIC) REFERENCES BANK(BIC)
                    );""")
            print("Table BANKDATA Created!")


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
                    (UID INTEGER,
                    STREET CHAR(50) NOT NULL,
                    NUMBER INTEGER NOT NULL,
                    POSTALCODE INTEGER NOT NULL,
                    CITY CHAR(50) NOT NULL,
                    FOREIGN KEY(UID) REFERENCES USER(UID)
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

    def complete_user(self, new_data: dict, token: str) -> str:

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
        
        
        # Get Check Private Data
        self.__curs.execute(f"""
                            SELECT *
                            FROM PRIVATE_DATA
                            WHERE UID='{uid}'
                            """)
        data_PD = self.__curs.fetchall()
        if len(data_PD) == 1:
            uid_tmp, birth, phone = data_PD[0]
            print(f"The User with the ID {uid}, has been found. Getting and Updating Data")
            sql_sttmnt_PD = f"UPDATE PRIVATE_DATA SET BIRTHDAY = ?, PHONE = ? WHERE UID={uid}"
            self.__curs.execute(sql_sttmnt_PD, [new_data["birthday"], new_data["phone"]])
        elif len(data_PD) > 1:
            print("Es wurden mehrer Nutzer mit der gleichen ID gefunden. Bitte wenden sie sich an ihren Andministrator!")
            return "ERROR"
        else:
            print(f"NO User with the id {uid}, has been found.Adding privata Data for this User")
            sql_sttmnt_PD = "INSERT INTO PRIVATE_DATA(UID, BIRTHDAY, PHONE) VALUES(?,?,?)"
            self.__curs.execute(sql_sttmnt_PD, [uid, new_data["birthday"], new_data["phone"]])
        
        
        # sql_sttmnt_ADDRESS = f"""INSERT OR REPLACE Into ADDRESS (UID, STREET, NUMBER, POSTALCODE, CITY) WHERE UID={uid} VALUES(?,?,?,?,?)"""
        # sql_sttmnt_BANK = f"""INSERT OR REPLACE Into BANK (BIC, Name) WHERE BIC={userinputbic} VALUES(?,?)"""
        # sql_sttmnt_BD = f"""INSERT OR REPLACE Into BANKDATA (UID, IBAN, BIC) VALUES(?,?,?)"""
        
        self.__db.commit()
        return uid

    def get_user(self, mail) -> list:
        self.__curs.execute(f"""
                            select 
                            USER.UID,
                            USER.NAME,
                            USER.FIRSTNAME,
                            USER.USERTOKEN,
                            USER.EMAIL,
                            PRIVATE_DATA.BIRTHDAY,
                            PRIVATE_DATA.PHONE,
                            ADDRESS.STREET,
                            ADDRESS.NUMBER,
                            ADDRESS.POSTALCODE,
                            ADDRESS.CITY,
                            BANKDATA.IBAN,
                            BANKDATA.BIC,
                            BANK.NAME
                             
                            from USER
                            LEFT JOIN PRIVATE_DATA
                            ON USER.UID = PRIVATE_DATA.UID
                            LEFT JOIN ADDRESS
                            ON USER.UID = ADDRESS.UID
                            LEFT JOIN BANKDATA
                            ON USER.UID = BANKDATA.UID
                            LEFT JOIN BANK
                            ON BANKDATA.BIC = BANK.BIC
                            WHERE USER.EMAIL='{mail}'
                            """)
        extracted_data = self.__curs.fetchall()
        self.__db.commit()
        return extracted_data


if __name__ == "__main__":
    db_test = Database_helper('Data/test.db')
    inp = ['test', 'Test12', 'h@b.de']
    # db_test.add_user(inp)
    # print(db_test.complete_user({"birthday": "20.08.2003", "phone": "0125468423543"}, "5ae0cb4d-5b28-417e-9658-971f37493814"))
    print(db_test.get_user('h@b.de'))
