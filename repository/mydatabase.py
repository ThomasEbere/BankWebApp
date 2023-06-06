import mysql.connector


class Database:

    def __int__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database

    @staticmethod
    def creatingconnection():
        user = 'root'
        password = ''
        host = '127.0.0.1'
        database = 'Vault'
        conn = mysql.connector.connect(user=user, password=password, host=host, database=database, buffered=True)
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE()")
        return conn

    @staticmethod
    def createdatabase():
        # Dropping database student if already exists.
        connect = Database.creatingconnection()
        cursor = connect.cursor()

        cursor.execute("Drop database if exists Vault")

        # Prepare query to create a database
        sql = "Create database Vault"

        # creating a database
        cursor.execute(sql)

        # Retrieving the list of databases
        cursor.execute("Show databases")

    @staticmethod
    def createtable():
        connect = Database.creatingconnection()
        cursor = connect.cursor()

        sql = """CREATE TABLE IF NOT EXISTS Account_Information(
            FIRST_NAME VARCHAR(20), LAST_NAME VARCHAR(20),
             email VARCHAR (30), Phone_Number VARCHAR (255), Address VARCHAR (50),
            PASSWORD VARCHAR(30),BALANCE INT, Confirmation_Code VARCHAR(20), STATUS BOOLEAN DEFAULT 0,
            PRIMARY KEY (email));
            """
        cursor.execute(sql)
        cursor.close()

    @staticmethod
    def insert_data(first_name, last_name, email, phone, address, password, balance, confirmation_code):
        connect = Database.creatingconnection()
        cursor = connect.cursor()
        INSERT_DATA = "INSERT INTO Account_Information(FIRST_NAME, LAST_NAME, email, phone_Number, address," \
                      "PASSWORD, BALANCE, Confirmation_Code) Values (%s,%s,%s,%s,%s,%s,%s, %s)"
        data = (first_name, last_name, email, phone, address, password, balance, confirmation_code)

        cursor.execute(INSERT_DATA, data)
        connect.commit()

    @staticmethod
    def getuser(email):
        connect = Database.creatingconnection()
        cursor = connect.cursor()
        getdata = "Select * from Account_Information where email=%s"
        cursor.execute(getdata, (email,))
        userdata = cursor.fetchone()
        if userdata:
            return list(userdata)
        return None

    @staticmethod
    def updateuserstatus(email):
        connect = Database.creatingconnection()
        cursor = connect.cursor()
        updatestatus = """UPDATE Account_Information SET STATUS=1 where email=%s"""
        cursor.execute(updatestatus, (email,))
        connect.commit()
        connect.close()
        return True

    @staticmethod
    def updateuserbalance(email, balance):
        connect = Database.creatingconnection()
        cursor = connect.cursor()
        updatebalance = """UPDATE Account_Information SET balance=%s where email=%s"""
        cursor.execute(updatebalance, (balance, email,))
        connect.commit()
        connect.close()
        return True

    @staticmethod
    def createbeneficiarytable():
        connect = Database.creatingconnection()
        cursor = connect.cursor()

        sql = """CREATE TABLE IF NOT EXISTS beneficiary_table(
            FIRST_NAME VARCHAR(20), LAST_NAME VARCHAR(20),
             email VARCHAR (30), created_by VARCHAR(30), PRIMARY KEY (email));"""
        cursor.execute(sql)
        cursor.close()

    @staticmethod
    def insert_beneficiary_data(first_name, last_name, email, created_by):
        connect = Database.creatingconnection()
        cursor = connect.cursor()
        INSERT_DATA = "INSERT INTO beneficiary_table(FIRST_NAME, LAST_NAME, email, created_by) Values (" \
                      "%s,%s,%s,%s)"
        data = (first_name, last_name, email, created_by)

        cursor.execute(INSERT_DATA, data)
        connect.commit()
        return True

    @staticmethod
    def getuserbeneficiary(email):
        connect = Database.creatingconnection()
        cursor = connect.cursor()
        getdata = "Select * from beneficiary_table where email=%s"
        cursor.execute(getdata, (email,))
        userdata = cursor.fetchone()
        if userdata:
            return list(userdata)
        return None

    @staticmethod
    def checkbeneficiary(email):
        connect = Database.creatingconnection()
        cursor = connect.cursor()
        getdata = "Select * from beneficiary_table where created_by=%s"
        cursor.execute(getdata, (email,))
        userdata = cursor.fetchall()
        if userdata:
            return list(userdata)
        return None




# Database.createtable()
Database.createbeneficiarytable()
# print(Database.getuser("thomasebere119@gmail.com"))
# Database.insert_data()
# print(Database.updateuserstatus("thomasebere119@gmail.com"))
