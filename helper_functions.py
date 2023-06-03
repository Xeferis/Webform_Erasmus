"""
Helper function for Erasmus Website Projekt

Contains:
Generate DB

Creator:    Florian Hillebold
"""
import sqlite3 as sq3
from uuid import uuid4


class Generate_db_user():
    """
    Generates all User-Databases
    and is used to manipulate
    """
    def __init__(self, path_2_db: str) -> None:
        """
        Initialize Databas and generate Tables if needed.

        Args:
            path_2_db (str): Path to databasefile
        """
        self.__db = sq3.connect(database=path_2_db)
        self.__curs = self.__db.cursor()
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
        """
        Add a User and generate a userspecific token

        Args:
            data (list): specified data as List containing
                            - Firstname
                            - Name
                            - e-Mail
            max_trys (int, optional): Try of loop trying to generate
                                      token. Defaults to 10.
        """
        sql_statement = """
                        INSERT INTO USER
                        (USERTOKEN,
                        FIRSTNAME,
                        NAME,
                        EMAIL
                        )
                        VALUES(?,?,?,?)
                        """
        loop_trys = 0

        if len(data) > 3:
            print("Too much data given!")
            return

        while True:
            token = str(uuid4())

            self.__curs.execute(f"""
                        SELECT count(USERTOKEN)
                        FROM USER
                        WHERE USERTOKEN='{token}'
                        """)

            if loop_trys > max_trys:
                print("Generating User ID failed. Abort adding User. \
                      no valid id has been found!")
                return
            elif self.__curs.fetchone()[0] == 1:
                print(f"ID: {token} already exists, generating new one!")
                loop_trys += 1
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

    def complete_user(self, new_data: dict, utoken: str) -> str:
        """
        Complete userdate with private information.

        Args:
            new_data (dict): Dict has to look like this
                                {
                                "birthday": date,
                                "phone": str,
                                "street": str,
                                "number": int,
                                "postal": int,
                                "city": str,
                                "iban": str,
                                "bic": str,
                                "bankbez": str
                                }
            utoken (str): usergenerated token out of the Database

        Returns:
            str: Returns the userid if succeful or "ERROR" if unsuccessful.
        """
        # Get UserID based on Token
        self.__curs.execute(f"""
                            SELECT *
                            FROM USER
                            WHERE USERTOKEN='{utoken}'
                            """)
        data = self.__curs.fetchall()
        if len(data) == 1:
            uid, token, name, fname, email = data[0]
            print(f"""
            The User with the token {utoken},
            has been found""")
        elif len(data) > 1:
            print("Es wurden mehrer Nutzer mit dem gleichen Token gefunden. \
                  Bitte wenden sie sich an ihren Andministrator!")
            return "ERROR"
        else:
            print(f"""
            NO User with the token {utoken},
            has been found""")
            return "ERROR"

        # Get/Check Private Data
        self.__curs.execute(f"""
                            SELECT *
                            FROM PRIVATE_DATA
                            WHERE UID='{uid}'
                            """)
        data_PD = self.__curs.fetchall()
        if len(data_PD) == 1:
            uid_tmp, birth, phone = data_PD[0]
            print(f"The User with the ID {uid}, has been found. \
                  Getting and Updating Data")

            sql_sttmnt_PD = f"""
                            UPDATE PRIVATE_DATA
                            SET
                            BIRTHDAY = ?,
                            PHONE = ?
                            WHERE UID={uid}
                            """

            self.__curs.execute(sql_sttmnt_PD, [
                new_data["birthday"],
                new_data["phone"]
                ])

        elif len(data_PD) > 1:
            print("Es wurden mehrer Nutzer mit der gleichen ID gefunden. \
                  Bitte wenden sie sich an ihren Andministrator!")
        else:
            print(f"NO User with the id {uid}, has been found. \
                  Adding privata Data for this User")

            sql_sttmnt_PD = """
                            INSERT INTO PRIVATE_DATA
                            (
                                UID,
                                BIRTHDAY,
                                PHONE
                            )
                            VALUES(?,?,?)"""

            self.__curs.execute(sql_sttmnt_PD, [
                uid,
                new_data["birthday"],
                new_data["phone"]
                ])

        # Get/Check Address
        self.__curs.execute(f"""
                            SELECT *
                            FROM ADDRESS
                            WHERE UID='{uid}'
                            """)
        data_AD = self.__curs.fetchall()

        if len(data_AD) == 1:
            uid_tmp, street, number, postal, city = data_PD[0]
            print(f"The User with the ID {uid}, has been found. \
                  Getting and Updating Data")

            sql_sttmnt_ADDRESS = f"""
                                UPDATE ADDRESS
                                SET
                                STREET = ?,
                                NUMBER = ? ,
                                POSTALCODE = ?,
                                CITY = ?
                                WHERE UID={uid}
                                """

            self.__curs.execute(sql_sttmnt_ADDRESS, [
                new_data["street"],
                new_data["number"],
                new_data["postal"],
                new_data["city"]
                ])

        elif len(data_AD) > 1:
            print("Es wurden mehrer Nutzer mit der gleichen ID gefunden. \
                  Bitte wenden sie sich an ihren Andministrator!")
        else:
            print(f"NO User with the id {uid}, has been found. \
                  Adding privata Data for this User")

            sql_sttmnt_ADDRESS = """
                                INSERT Into ADDRESS
                                (
                                    UID,
                                    STREET,
                                    NUMBER,
                                    POSTALCODE,
                                    CITY
                                )
                                VALUES(?,?,?,?,?)
                                """
            self.__curs.execute(sql_sttmnt_ADDRESS, [
                uid,
                new_data["street"],
                new_data["number"],
                new_data["postal"],
                new_data["city"]
                ])

        # Get/Check Bankdata
        self.__curs.execute(f"""
                            SELECT *
                            FROM BANKDATA
                            WHERE UID='{uid}'
                            """)
        data_BD = self.__curs.fetchall()

        if len(data_BD) == 1:
            UID, iban, bic = data_BD[0]

            print(f"The User with the ID {uid}, has been found. \
                  Getting and Updating Data")

            sql_sttmnt_BD = f"""
                            UPDATE BANKDATA
                            SET
                            IBAN = ?,
                            BIC = ?
                            WHERE UID={uid}
                            """

            self.__curs.execute(sql_sttmnt_BD, [
                new_data["iban"],
                new_data["bic"]
                ])

        elif len(data_BD) > 1:
            print("Es wurden mehrer Nutzer mit der gleichen ID gefunden. \
                  Bitte wenden sie sich an ihren Andministrator!")
        else:
            print(f"NO User with the id {uid}, has been found. \
                  Adding privata Data for this User")

            sql_sttmnt_BD = """
                            INSERT Into BANKDATA
                            (
                                UID,
                                IBAN,
                                BIC
                            )
                            VALUES(?,?,?)
                            """

            self.__curs.execute(sql_sttmnt_BD, [
                uid,
                new_data["iban"],
                new_data["bic"]
                ])

        # Get/Check Bank
        self.__curs.execute(f"""
                            SELECT *
                            FROM BANK
                            WHERE BIC='{new_data['bic']}'
                            """)
        data_B = self.__curs.fetchall()

        if len(data_B) == 1:
            bic, name = data_BD[0]
            print(f"The Bank with the BIC {new_data['bic']}, already exists.")
        elif len(data_B) > 1:
            print("Es wurden mehrer Banken mit der gleichen BIC gefunden. \
                  Bitte wenden sie sich an ihren Andministrator!")
        else:
            print(f"NO BANK with the bic {new_data['bic']}, has been found. \
                  Adding privata Data for this User")

            sql_sttmnt_BANK = """
                            INSERT Into BANK
                            (
                                BIC,
                                Name
                            )
                            VALUES(?,?)
                            """

            self.__curs.execute(sql_sttmnt_BANK, [
                new_data["bic"],
                new_data["bankbez"]
                ])

        self.__db.commit()
        return uid

    def get_user(self, mail: str) -> list:
        """
        Returns all Userdate by inputing the Mail

        Args:
            mail (str): Usermailaddress

        Returns:
            list: returns a List of all Informations
            for that specific user
        """
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

    def del_user(self, utoken: str) -> None:
        """
        Delets all user specific Data

        Args:
            utoken (str): UUID of the User that should be deleted!
        """
        # Get UserID based on Token
        self.__curs.execute(f"""
                            SELECT *
                            FROM USER
                            WHERE USERTOKEN='{utoken}'
                            """)
        data = self.__curs.fetchall()
        if len(data) == 1:
            uid, token, name, fname, email = data[0]
            print(f"""
            The User with the token {utoken},
            has been found and gets deleted""")

            self.__curs.execute(f"""
                            DELETE
                            from USER
                            WHERE USER.UID='{uid}'
                            """)

            self.__curs.execute(f"""
                                DELETE
                                from PRIVATE_DATA
                                WHERE PRIVATE_DATA.UID='{uid}'
                                """)

            self.__curs.execute(f"""
                                DELETE
                                from ADDRESS
                                WHERE ADDRESS.UID='{uid}'
                                """)

            self.__curs.execute(f"""
                                DELETE
                                from BANKDATA
                                WHERE BANKDATA.UID='{uid}'
                                """)
        elif len(data) > 1:
            print("Es wurden mehrer Nutzer mit dem gleichen Token gefunden. \
                  Bitte wenden sie sich an ihren Andministrator!")
        else:
            print(f"NO User with the token {utoken}, \
            has been found. It might be deleted already")
        self.__db.commit()


class Generate_db_admin():
    """
    Generates all Admin-Databases
    and is used to manipulate
    """
    def __init__(self, path_2_db: str) -> None:
        """
        ADMIN
        Initialize Database and generate Tables if needed.

        Args:
            path_2_db (str): Path to databasefile
        """
        self.__db = sq3.connect(database=path_2_db)
        self.__curs = self.__db.cursor()
        self.__tokenlength = 16

        # Check and/or create ADMIN Table
        self.__curs.execute("""
                    SELECT count(name)
                    FROM sqlite_master
                    WHERE type='table'
                    AND name='ADMIN'
                    """)

        if self.__curs.fetchone()[0] == 1:
            print("Table ADMIN exists")
        else:
            self.__curs.execute("""
                    CREATE TABLE ADMIN
                    (AUID INTEGER PRIMARY KEY AUTOINCREMENT,
                    USERNAME CHAR(32) NOT NULL,
                    FIRSTNAME CHAR(20) NOT NULL,
                    NAME CHAR(20) NOT NULL,
                    EMAIL CHAR(25) NOT NULL,
                    PASSWORD CHAR(16) NOT NULL
                    );""")
            print("Table ADMIN Created!")

    def add_admin(self, data: list) -> None:
        """
        Add a User and generate a userspecific token

        Args:
            data (list): specified data as List containing
                            - Username
                            - Firstname
                            - Name
                            - e-Mail
                            - Passwort
        """
        sql_statement = """
                        INSERT INTO ADMIN
                        (USERNAME,
                        FIRSTNAME,
                        NAME,
                        EMAIL,
                        PASSWORD
                        )
                        VALUES(?,?,?,?,?)
                        """

        if len(data) > 5:
            print("Too much data given!")
            return

        self.__curs.execute(f"""
                        SELECT count(EMAIL)
                        FROM ADMIN
                        WHERE EMAIL='{data[3]}'
                        """)

        if self.__curs.fetchone()[0] == 1:
            print(f"Admin with the EMAIL: {data[3]} already exists")
            print("No Admin added")
            self.__db.commit()
        else:
            print(f"Adding new Admin with Username {data[0]}")
            self.__curs.execute(sql_statement, data)
            self.__db.commit()

    def get_admin(self, mail: str) -> list:
        """
        Returns all Admindata by inputing the Mail

        Args:
            mail (str): Adminusermailaddress

        Returns:
            list: returns a List of all Informations
            for that specific Admin
        """
        self.__curs.execute(f"""
                            SELECT *
                            FROM ADMIN
                            WHERE EMAIL='{mail}'
                            """)
        extracted_data = self.__curs.fetchall()
        self.__db.commit()
        if len(extracted_data) > 0:
            return extracted_data
        else:
            return "No Admin has been found"

    def change_pw(self, username: str, email: str, old_pw: str, new_pw: str) -> None:
        """
        Changing the Admin password of an existing Admin

        Args:
            username (str): username of the admin that would change the password
            email (str): email of the admin that would change the password
        """
        self.__curs.execute(f"""
                        SELECT *
                        FROM ADMIN
                        WHERE USERNAME='{username}'
                        AND EMAIL='{email}'
                        """)

        data = self.__curs.fetchall()
        if len(data) == 1:
            print(f"Admin with the EMAIL: {email} has been found")
            auid, username, name, fname, email, pw = data[0]
            if pw == old_pw:
                print("The entered Password was correct")
                sql_stmnt = f"""
                            UPDATE ADMIN
                            SET
                            PASSWORD = ?
                            WHERE AUID={auid}
                            """
                self.__curs.execute(sql_stmnt, [new_pw])
            else:
                print("The entered Password was incorrect")
        self.__db.commit()

    def del_admin(self, username: str, email: str, pw: str) -> None:
        """
        Delets all Admin specific Data

        Args:
            pw (str): Password of the Admin that should be deleted!
            username (str): Username of the Admin that should be deleted!
        """
        # Get UserID based on Token
        self.__curs.execute(f"""
                            SELECT *
                            FROM ADMIN
                            WHERE PASSWORD='{pw}'
                            AND USERNAME='{username}'
                            AND EMAIL='{email}'
                            """)
        data = self.__curs.fetchall()
        if len(data) == 1:
            auid, username, name, fname, email, pw = data[0]
            print(f"""
            The Admin with the Username {username},
            has been found and gets deleted""")

            self.__curs.execute(f"""
                            DELETE
                            from ADMIN
                            WHERE ADMIN.AUID='{auid}'
                            """)

        elif len(data) > 1:
            print("Es wurden mehrer Nutzer mit dem gleichen Username gefunden. \
                  Bitte wenden sie sich an ihren Keyuser!")
        else:
            print(f"No Admin with the Username: {username}, \
            has been found. It might be deleted already")
        self.__db.commit()


def test_user_db():
    db_test = Generate_db_user('Data/test.db')
    inp = ['test', 'Test12', 'h@b.de']
    new_data = {
        "birthday": "20.08.2003",
        "phone": "0125468423543",
        "street": "TestStreet",
        "number": 18,
        "postal": 45438,
        "city": "testhausen",
        "iban": "DE45 2341 1233 1673 0000 44",
        "bic": "GENODIX23",
        "bankbez": "Deutsche Test Bank eV"
        }
    # db_test.add_user(inp)
    # print(db_test.complete_user(new_data, "ca883e0a-192a-467e-a61e-128a57c0806a"))
    print(db_test.get_user('h@b.de'))
    db_test.del_user("ca883e0a-192a-467e-a61e-128a57c0806a")
    # print(db_test.get_user('h@b.de'))


def test_admin_db():
    db_test = Generate_db_admin('Data/test_ad.db')
    inp = ['TestUsername', 'admn_test', 'admn_Test12', 'admn_h@b.de', 'sdfj1ud783']

    # Add Test
    # db_test.add_admin(inp)
    print(db_test.get_admin('admn_h@b.de'))

    # Del Test
    # db_test.del_admin('TestUsername',
    #                   'admn_h@b.de',
    #                   'sdfj1ud783')
    # print(db_test.get_admin('admn_h@b.de'))

    # Change PW
    # db_test.change_pw('TestUsername', 'admn_h@b.de', 'sdfj1ud783', 'dksjhf82')
    # print(db_test.get_admin('admn_h@b.de'))


if __name__ == "__main__":
    # test_user_db()
