from flask_mysqldb import MySQL
#from codes.DatabaseUtil import InitializeData
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, url_for
#from flask_login import login_user
import os
import sys

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'dijkstra.ug.bcc.bilkent.edu.tr'
app.config['MYSQL_USER'] = 'sena.yilmaz'
app.config['MYSQL_PASSWORD'] = '97hws1Lr'
app.config['MYSQL_DB'] = 'sena_yilmaz'

mysql = MySQL(app)

@app.route('/')
@app.route('/indexpage')
def indexpage():
	return render_template('index.html')

@app.route('/loginpage', methods=["GET", "POST"])
def loginpage():
    data = []
    if (request.method == 'POST'):
	    username = request.form['username']
	    password = request.form['password']

	    cur = mysql.connection.cursor()
	    cur.execute("select * from Hotel_Users where username='" + username + "' and password='" + password + "'")
        
    for row in cur :
        data.append(row)

    if (len(data)>0):
        user_id = data[0]
        session['user_id'] = user_id[0]
        return redirect(url_for('guesthomepage'))

    else:
        flash("Error")
        return render_template('wronglogin.html')

@app.route('/registerpage', methods=["GET", "POST"])
def registerpage():
	if request.method == 'GET':
		return render_template('register.html')
	else:
		username = request.form['username']
		password = request.form['password']
		bdate = request.form['bdate']
		gender = request.form['gender']
		address = request.form['address']

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO Hotel_Users (username, password, bdate, gender, address) VALUES ('" + username + "','" + password + "','" + bdate + "','" + gender + "','" + address + "')")
		mysql.connection.commit()

		return render_template('index.html')

@app.route('/guesthomepage', methods=["GET", "POST"])
def guesthomepage():
	user_id = session['user_id']
	if request.method == 'GET':

		cur = mysql.connection.cursor()
		cur.execute("select * from Reservation where user_ID='" + str(user_id) + "'")
		data = cur.fetchall()
		cur.execute("select username from Hotel_Users where user_ID='" + str(user_id) + "'")
		name = cur.fetchone()

		return render_template('guesthomepage.html', data=data, name=name)

@app.route('/bookreservationpage', methods=["GET", "POST"])
def bookreservationpage():
	if request.method == 'GET':
		return render_template('bookreservation.html')
	else:
		check_in_date = request.form['check_in_date']
		check_out_date = request.form['check_out_date']
		numOfStayers = request.form['numOfStayers']

		cur = mysql.connection.cursor()
		#price = ((check_out_date - check_in_date).days )*(numOfStayers*150)
		user_id = session['user_id']
		price = 3000
		cur.execute("INSERT INTO Reservation (reservation_date, check_in_date, check_out_date, numOfStayers, price, user_ID) VALUES (CURDATE(), '" + check_in_date + "','" + check_out_date + "','" + str(numOfStayers) + "', '" + str(price) + "', '" + str(user_id) + "')")
		mysql.connection.commit()

		return redirect(url_for('guesthomepage'))


@app.route('/foodorders', methods=["GET", "POST"])
def foodorders():
	user_id = session['user_id']
	orderdata =[]
	fooddata = []
	if request.method == 'GET':
		cur = mysql.connection.cursor()
		cur.execute("select order_id,order_date,food_id from Orders where user_ID='" + str(user_id) + "'")
		orders = cur.fetchall()
		return render_template('foodorders.html', orders=orders)
	
	else:
		orderid = request.form['selectedorderid']
		cur = mysql.connection.cursor()
		cur.execute("select order_date,food_id from Orders where order_id='" + str(orderid) + "'")

		for row in cur:
			orderdata.append(row)
		orderdate = orderdata[0][0]
		foodid = orderdata[0][1]

		cur.execute("SELECT restaurant_id,food_name,food_price from Food where food_id='"  + str(foodid) + "'")
		for row in cur:
			fooddata.append(row)
		
		restaurantID = fooddata[0][0]
		foodName = fooddata[0][1]
		foodPrice = fooddata[0][2]
		return render_template('fooddetails.html', orderdate = orderdate, restaurantID = restaurantID, foodName=foodName, foodPrice=foodPrice )


@app.route('/newfoodorder', methods=["GET", "POST"])
def newfoodorder():
	user_id = session['user_id']
	if request.method == 'GET':
		cur = mysql.connection.cursor()
		cur.execute("select food_id,food_name,food_price from Food where restaurant_id='" + str(1) + "'")
		restaurant1 = cur.fetchall()
		cur.execute("select food_id,food_name,food_price from Food where restaurant_id='" + str(2) + "'")
		restaurant2 = cur.fetchall()
		cur.execute("select food_id,food_name,food_price from Food where restaurant_id='" + str(3) + "'")
		restaurant3 = cur.fetchall()

		return render_template('newfoodorder.html', restaurant1=restaurant1,restaurant2=restaurant2,restaurant3=restaurant3 )

	else:
		foodid = request.form['selectedfoodid']
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO Orders (order_date, user_ID, food_id) VALUES (" + "CURDATE()" + ",'" + str(user_id) +"','"+str(foodid) +"')")
		mysql.connection.commit()
		return redirect(url_for('guesthomepage'))



@app.route('/buyticket', methods=["GET", "POST"])
def buyticket():
	if request.method == 'GET':
		return render_template('buyticket.html')

@app.route('/shopping', methods=["GET", "POST"])
def shopping():
	if request.method == 'GET':
		return render_template('shopping.html')


@app.route('/leavecomment', methods=["GET", "POST"])
def leavecomment():
	if request.method == 'GET':
		return render_template('leavecomment.html')



if __name__ == "__main__":
	app.secret_key = os.urandom(16)
	app.run(debug=True)