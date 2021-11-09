from flask import *
import random
import hashlib
import mysql.connector

app = Flask(__name__)

@app.route('/signup', methods=['GET'])
def signUp():
    con = mysql.connector.connect(host='scislearn3.uohyd.ac.in', database='uohvams',user='phpmyadmin', password='passwd@123')
    cursor = con.cursor()
    emp_id = request.args.get('emp_id')
    name = request.args.get('name')
    email = request.args.get('email')
    password = request.args.get('password')
    data = (emp_id,name,email,password,)
    query = "insert into User_table (emp_id, name, email, password) values (%s,%s,%s,%s)"
    cursor.execute(query, data)
    con.commit()
    cursor.close()
    con.close()
    print("Success")
    return "Data inserted successfully"

@app.route('/signin',methods=['GET'])
def signIn():
    con = mysql.connector.connect(host='scislearn3.uohyd.ac.in', database='uohvams',user='phpmyadmin', password='passwd@123')
    cursor = con.cursor()
    emp_id = request.args.get('emp_id')
    name = request.args.get('name')
    in_out = request.args.get('in_out')
    query = "insert into Logs (emp_id, name, in_out) values (%s, %s, %s)"
    data = (emp_id, name, in_out,)
    cursor.execute(query, data)
    con.commit()
    cursor.close()
    con.close()
    print("Logged successfully")
    return "Logged successfully"


@app.route('/geolog',methods=['GET'])
def geoLog():
    con = mysql.connector.connect(host='scislearn3.uohyd.ac.in', database='uohvams',user='phpmyadmin', password='passwd@123')
    cursor = con.cursor()
    emp_id = request.args.get('emp_id')
    name = request.args.get('name')
    loc_id = request.args.get('loc_id')
    in_out = request.args.get('in_out')
    query = "insert into Geo_logs (emp_id, name, loc_id, in_out) values (%s, %s, %s, %s)"
    data = (emp_id, name, loc_id, in_out, )
    cursor.execute(query, data)
    con.commit()
    cursor.close()
    con.close()
    print("logged at ",loc_id)
    return loc_id

#TODO: Make it work
@app.route('/checkemp',methods=['GET'])
def checkEmp():
    con = mysql.connector.connect(host='scislearn3.uohyd.ac.in', database='uohvams',user='phpmyadmin', password='passwd@123')
    cursor = con.cursor()
    query = "select * from User_table where emp_id = %s"
    data = (request.args.get('id'),)
    cursor.execute(query, data)
    rows = cursor.fetchall()
    if(len(rows) != 0):
        return "Old User"
    else:
        return "New User"

@app.route('/getname',methods=['GET'])
def getName():
    con = mysql.connector.connect(host='scislearn3.uohyd.ac.in', database='uohvams',user='phpmyadmin', password='passwd@123')
    cursor = con.cursor()
    query = "select * from User_table where emp_id = %s"
    data = (request.args.get('id'),)
    cursor.execute(query, data)
    rows = cursor.fetchone()
    if(rows):
        print(rows[2])
        return rows[2]
    else:
        return

@app.route('/generatetoken',methods=['GET'])
def generateToken():
    # con = mysql.connector.connect(host='remotemysql.com',database='cVLw2NAjNX',user='cVLw2NAjNX',password='7I3RP65o9I')
    con = mysql.connector.connect(host='scislearn3.uohyd.ac.in', database='uohvams',user='phpmyadmin', password='passwd@123')
    # con = mysql.connector.connect(host='sql6.freesqldatabase.com',database='sql6438285',user='sql6438285',password='mhsxG3lpiD')
    cursor = con.cursor()
    clientid = (request.args.get('id'),)
    query1 = "select * from oAuth where client_id = %s"
    cursor.execute(query1, clientid)
    rows = cursor.fetchall()
    if(len(rows) != 0):
        query2 = "insert into tokens (client_id, token) values (%s,%s)"
        k = random.randint(0,199999)
        s = str(k)
        token = hashlib.sha224(s.encode()).hexdigest()
        data = (request.args.get('id'),token)
        cursor.execute(query2, data)
        con.commit()
        cursor.close()
        con.close()
        print(token)
        return token
    else:
        print("Invalid client")
        return "Invalid client"

@app.route('/createclient',methods=['GET'])
def createClient():
    con = mysql.connector.connect(host='scislearn3.uohyd.ac.in', database='uohvams',user='phpmyadmin', password='passwd@123')
    # con = mysql.connector.connect(host='remotemysql.com',database='cVLw2NAjNX',user='cVLw2NAjNX',password='7I3RP65o9I')
    # con = mysql.connector.connect(host='sql6.freesqldatabase.com',database='sql6438285',user='sql6438285',password='mhsxG3lpiD')
    cursor = con.cursor()
    query = "insert into oAuth (emp_id, client_id) values (%s,%s)"
    k = random.randint(0,19999)
    s = str(k)
    client = hashlib.sha256(s.encode()).hexdigest()
    data = (request.args.get('id'),client)
    cursor.execute(query, data)
    con.commit()
    cursor.close()
    con.close()
    return client

@app.route('/authorize',methods=['GET'])
def authorizeToken():
    # con = mysql.connector.connect(host='sql6.freesqldatabase.com',database='sql6438285',user='sql6438285',password='mhsxG3lpiD')
    con = mysql.connector.connect(host='scislearn3.uohyd.ac.in', database='uohvams',user='phpmyadmin', password='passwd@123')
    # con = mysql.connector.connect(host='remotemysql.com',database='cVLw2NAjNX',user='cVLw2NAjNX',password='7I3RP65o9I')
    cursor = con.cursor()
    query = "select * from tokens where token = %s"
    data=(request.args.get('token'),)
    cursor.execute(query, data)
    rows = cursor.fetchall()
    if(len(rows) != 0):
        return "valid token"
    else:
        return "invalid token"

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8090,debug=False)