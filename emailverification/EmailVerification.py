import sqlite3
#import mysql, connector
from flask import Flask, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


app = Flask(__name__)
#recieving sending credentials from this file
app.config.from_pyfile('config.cfg')


	

mail = Mail(app)

s = URLSafeTimedSerializer('Thisisasecret!')

@app.route('/', methods=['GET', 'POST'])
def index():
	
	if request.method == 'GET':
		return '<form action="/" method="POST"><input name="email"><input type="submit"></form>'
	#recieves email from user
	email = request.form['email']
	db = sqlite3.connect('verified.db')
	cursor = db.cursor()

	# cursor.execute('''ALTER TABLE accounts
	# ADD COLUMN IF NOT EXISTS token VARCHAR(100)''')
	
	token = s.dumps(email, salt='email-confirm')
	
	verified = 1
	#puts in default value for email entered by user. Verified status is set to 0, hence it hasnt been verified
	cursor.execute('INSERT INTO accounts VALUES(?,?,?)',(email,verified,token))
	#specifies sender and reciever
	msg = Message('Confirm Email', sender='pbbetatest@gmail.com', recipients=[email])
 	#generates url token for user.
	link = url_for('confirm_email', token=token, _external=True)
	#user recieves this link in thier inbox. CLicking on the link verifies them
	msg.body = 'Your link is {}'.format(link)
	#finnally sends the message
	mail.send(msg)
	#connects to database with emails and their verified status
	db.commit()
	db.close()

	return '<h1>The email you entered is {}. The token is {}</h1>'.format(email, token)
#on clicking the link
@app.route('/confirm_email/<token>')
def confirm_email(token):

	email = s.loads(token, salt='email-confirm')

	#email= str(email)
	#connecting to database again
	db = sqlite3.connect('verified.db')
	cursor = db.cursor()
	#creating table with the email and verified status
	cursor.execute('CREATE TABLE IF NOT EXISTS accounts (email string, verified int, token char)')
	
	
	
	#adding email to database

	#once email has been verified, verified column is set to 1
	cursor.execute('''UPDATE accounts SET verified= 1
	WHERE verified = 0''')
	cursor.execute('''UPDATE accounts SET token = token
	WHERE token = "kko"''')

	#print(row[1])
	db.commit()
	db.close()
	print("doing the needful")
	
	#return message once the confirmation link has been clicked
	return '<h1>email verified</h1>'

	
# def getEmail():
# 	db = sqlite3.connect('ifiedemail.db')
# 	cursor = db.cursor()
		
# 	cursor.execute('CREATE TABLE IF NOT EXISTS accounts (email text, verified int)')
	


	
# 	email = "kaustinight1@gmail.com"
# 	myresult = cursor.fetchall()

# 	for row in myresult:
# 		if email in row:
# 			if row[2] == 0:
# 				cursor.execute('''UPDATE accounts SET verified = 1
# 				WHERE verified = 0''')
# 				cursor.execute('''UPDATE accounts SET email = "g"
# 				WHERE email = NULL''')

# 	#print(row[1])
# 	db.commit()
# 	db.close()
# #getEmail()
	


if __name__ == '__main__':
	app.run(debug=True)
	