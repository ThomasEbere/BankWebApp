from repository import mydatabase
from users.generatedID import UserId

connection = mydatabase.Database()


class User:
    newuserid = UserId.generaterandom()

    def __init__(self, first_name, last_name, email, phonenumber, address, password, userid):
        self.firstname = first_name
        self.lastname = last_name
        self.email = email
        self.phonenumber = phonenumber
        self.address = address
        self.password = password
        self.balance = 1000
        self.userid = userid

    def createaccount(self):
        connection.insert_data(self.firstname, self.lastname, self.email, self.phonenumber, self.address,
                               self.password,
                               self.balance, self.userid)
        return True
# connection = User("James", "Adam", "thomasebere119@gmail.com", 2269724000, "255 Sunview", "Prick123")
# connection.createaccount()
