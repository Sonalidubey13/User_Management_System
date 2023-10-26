# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import json

app = Flask(__name__)


app.secret_key = 'your secret key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sonali@123' #Put your password here
app.config['MYSQL_DB'] = 'demo'


mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(
			'SELECT * FROM accounts WHERE username = % s \
			AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			session['role'] = account['role']
			session['status'] = account['status']
			print(session['status'])
			# msg = 'Logged in successfully !'
			if session['status'] == 'Active':
				msg = 'Logged in successfully !'
				return render_template('index.html', msg=msg)
			else:
				msg = 'Pending Admin Approval !'
				# return render_template('index.html', msg=msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():


    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and	'email' in request.form and 'userid' in request.form and 'process' in request.form and	'accountname' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		userid = request.form['userid']
		process = request.form['process']
		accountname = request.form['accountname'] 
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(
			'SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'name must contain only characters and numbers !'
		else:
			query=f'''Insert into accounts (id,username,password,email,userid,process,accountname, role ,supervisorid, status) values (NULL,'{username}','{password}',
			'{email}','{userid}','{process}','{accountname}',NULL,NULL,NULL)'''
			print(query,"hellooworkd")
			cursor.execute(query)
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg=msg)


@app.route("/index")
def index():
	if 'loggedin' in session:
		return render_template("index.html")
	return redirect(url_for('login'))


@app.route("/existingUser")
def existingUser():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		query = f"Select * from accounts"		
		cursor.execute(query)
		data = cursor.fetchall()
		mysql.connection.commit()
		return render_template("existingUser.html",data=data)
	return redirect(url_for('login'))

@app.route("/delete",methods=['GET', 'POST'])
def delete():
	username = request.data
	username=json.loads(username)
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		query=f"Delete from accounts where username = '{username}'"
		print('hi dlee',username)
		print(query)
		cursor.execute(query)
		mysql.connection.commit()
		msg = 'Success'
		return render_template("existingUser.html",msg=msg)
	return redirect(url_for('login'))

@app.route("/disable",methods=['GET', 'POST'])
def disable():
	username = request.data
	username=json.loads(username)
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		query=f"UPDATE accounts SET status = 'Inactive' where username = '{username}'"
		print('hi dlee',username)
		print(query)
		cursor.execute(query)
		mysql.connection.commit()
		msg = 'Success'
		return render_template("existingUser.html",msg=msg)
	return redirect(url_for('login'))



@app.route("/display")
def display():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE id = % s',
					(session['id'], ))
		account = cursor.fetchone()
		return render_template("display.html", account=account)
	return redirect(url_for('login'))


@app.route("/update", methods=['GET', 'POST'])
def update():
	msg = ''
	if 'loggedin' in session:
		if request.method == 'POST' and 'username' in request.form and 'password' in request.form and	'email' in request.form and 'userid' in request.form and 'process' in request.form and	'accountname' in request.form :
			username = request.form['username']
			password = request.form['password']
			email = request.form['email']
			userid = request.form['userid']
			process = request.form['process']
			accountname = request.form['accountname'] 
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute(
				'SELECT * FROM accounts WHERE username = % s',
					(username, ))
			account = cursor.fetchone()
			if account:
				msg = 'Account already exists !'
			elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
				msg = 'Invalid email address !'
			elif not re.match(r'[A-Za-z0-9]+', username):
				msg = 'name must contain only characters and numbers !'
			else:
				cursor.execute('UPDATE accounts SET username =% s,\
				password =% s, email =% s, userid =% s, \
				process =% s, accountname =% s WHERE id =% s', (
					username, password, email, userid, 
				process, accountname,  
				(session['id'], ), ))

				mysql.connection.commit()

				msg = 'You have successfully updated !'
		elif request.method == 'POST':
			msg = 'Please fill out the form !'
		return render_template("update.html", msg=msg)
	return redirect(url_for('login'))


if __name__ == "__main__":
	app.run(host="localhost", port=int("5000"))
