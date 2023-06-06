from flask import Flask, render_template, request, redirect, url_for, session, flash
from users.Users import User
from users.generatedID import UserId
from SendEmailService import Email
from repository import mydatabase

app = Flask(__name__)
app.secret_key = 'myString'

send = Email.SendEmail()

dataaccess = mydatabase.Database()


@app.route("/", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        firstname = request.form['first_name']
        lastname = request.form['last_name']
        email = request.form['email']
        address = request.form['address']
        phonenumber = request.form['phonenumber']
        password = request.form['password']
        connect = User(firstname, lastname, email, phonenumber, address, password, send.confirmation_code)
        if connect.createaccount():
            if send.accountcreation(email, firstname):
                return render_template('confirmation.html')

    return render_template("signup.html")


@app.route("/confirmation/<email>/<myid>")
def confirmaccount(email, myid):
    userdata = dataaccess.getuser(email)
    print(userdata[7], myid)
    if userdata[7] == myid:
        if dataaccess.updateuserstatus(email):
            return redirect(url_for('login'))

        return "Sorry we could not authenticate you"


@app.route("/login", methods=['POST', 'GET'])
def login():
    if 'email' in session:
        return redirect(url_for('homepage'))
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        print(email, password)
        userdata = dataaccess.getuser(email)
        error = None
        emailerror = None
        if userdata is not None:
            if userdata[5] == password:
                session['email'] = userdata[2]
                print(session['email'])
                print("Got here")
                return redirect(url_for('homepage'))
            else:
                error = "Incorrect Password. PLease Try again"
                return render_template('login.html', error=error)
        emailerror = "User with this email and password does not exist"
        return render_template('login.html', emailerror=emailerror)
    return render_template('login.html')


@app.route("/homepage")
def homepage():
    if 'email' in session:
        email = session['email']
        userdata = dataaccess.getuser(email)
        name = userdata[0]
        return render_template('homepage.html', name=name)
    return redirect(url_for('login'))


@app.route("/transact")
def transact():
    if 'email' in session:
        email = session['email']
        userdata = dataaccess.getuser(email)
        name = userdata[0]
        return render_template("transactionspage.html", name=name)
    return redirect(url_for('login'))


@app.route("/transact/withdraw", methods=['POST', 'GET'])
def withdraw():
    if 'email' in session:
        email = session['email']
        if request.method == "POST":
            amount = request.form['amount']
            print(amount)
            userdata = dataaccess.getuser(email)
            print(userdata[6])
        return render_template("withdraw.html")
    return redirect(url_for('login'))


@app.route("/transact/balance")
def balance():
    if 'email' in session:
        email = session['email']
        userinfo = dataaccess.getuser(email)
        balance = userinfo[6]
        return render_template('balance.html', balance=balance)
    return redirect(url_for('login'))


@app.route("/transact/deposit", methods=['POST', 'GET'])
def deposit():
    if 'email' in session:
        email = session['email']
        if request.method == 'POST':
            amount = request.form['amount']
            print("Request got here")
            print(amount)
            userinfo = dataaccess.getuser(email)
            balance = userinfo[6]
            newbalance = balance + int(amount)
            dataaccess.updateuserbalance(email, newbalance)
            send.deposit(email, amount, userinfo[0], userinfo[0])
            return render_template('after-transaction.html')

        return render_template("deposit.html")
    return redirect(url_for('login'))


@app.route("/transact/transfer", methods=['POST', 'GET'])
def transfer():
    error = None
    if 'email' in session:
        email = session['email']
        if dataaccess.checkbeneficiary(email):
            userdata = dataaccess.checkbeneficiary(email)
            return render_template('transferpage.html', userdata=userdata)

        else:
            return render_template('transfer.html')
    return redirect(url_for('login'))


@app.route("/transact/transfer/<receiveremail>", methods=['POST', 'GET'])
def performtransfer(receiveremail):
    if 'email' in session:
        receiverdata = dataaccess.getuser(receiveremail)
        if request.method == 'POST':
            useremail = session['email']
            amount = request.form['amount']
            sendersdata = dataaccess.getuser(useremail)
            if sendersdata[6] > int(amount):
                if dataaccess.getuser(receiveremail):
                    newbalance = sendersdata[6] - int(amount)
                    newamount = receiverdata[6] + int(amount)
                    dataaccess.updateuserbalance(useremail, newbalance)
                    dataaccess.updateuserbalance(receiveremail, newamount)
                    send.deposit(receiverdata[2], amount, receiverdata[0], useremail)
                    send.transfer(sendersdata[0], amount,sendersdata[2] , receiverdata[0])
                    print("reach here")
                    return render_template('after-transaction.html')
                else:
                    flash('This user email does not exist in our records.')
                    return render_template('transfer.html')
            else:
                flash('Insufficient  balance')
                return render_template('transfer.html')
        return render_template("transfer_records.html", receiverdata=receiverdata)
    return redirect(url_for('login'))


@app.route('/test')
def test():
    return render_template('home.html')


@app.route('/transact/add-beneficiary', methods=['POST', 'GET'])
def addbeneficiary():
    if 'email' in session:
        if request.method == 'POST':
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            beneficiary_email = request.form['email']
            email = session['email']
            amount = request.form['amount']
            print(amount)
            sendersdata = dataaccess.getuser(email)
            if sendersdata[6] > int(amount):
                if dataaccess.getuser(beneficiary_email):
                    newbalance = sendersdata[6] - int(amount)
                    receiverdata = dataaccess.getuser(beneficiary_email)
                    newamount = receiverdata[6] + int(amount)
                    dataaccess.updateuserbalance(email, newbalance)
                    dataaccess.updateuserbalance(beneficiary_email, newamount)
                    send.deposit(receiverdata[2], amount, receiverdata[0], email)
                    send.transfer(sendersdata[0], amount, beneficiary_email, receiverdata[0])
                    if dataaccess.getuserbeneficiary(beneficiary_email):
                        return render_template("after-transaction.html")
                    else:
                        dataaccess.insert_beneficiary_data(firstname, lastname, beneficiary_email, email)
                        return render_template("after-transaction.html")
                else:
                    flash('This user email does not exist in our records')
                    return render_template('transfer.html')
            else:
                flash('Insufficient  balance')
                return render_template('transfer.html')
        return render_template('transfer.html')
    return redirect(url_for('login'))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True, port=4100)
