from flask import *
import random
import hashlib
import mysql.connector

app = Flask(__name__)

@app.route('/generatetoken',methods=['GET'])
def generateToken():
    con = mysql.connector.connect(host='remotemysql.com',database='cVLw2NAjNX',user='cVLw2NAjNX',password='7I3RP65o9I')
    cursor = con.cursor()
    query = "insert into tokens (client_id, token) values (%s,%s)"
    k = random.randint(0,199999)
    s = str(k)
    token = hashlib.sha224(s.encode()).hexdigest()
    data = (request.args.get('id'),token)
    cursor.execute(query, data)
    con.commit()
    cursor.close()
    con.close()
    print(token)
    return token

@app.route('/createclient',methods=['GET'])
def createClient():
    con = mysql.connector.connect(host='remotemysql.com',database='cVLw2NAjNX',user='cVLw2NAjNX',password='7I3RP65o9I')
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
    con = mysql.connector.connect(host='remotemysql.com',database='cVLw2NAjNX',user='cVLw2NAjNX',password='7I3RP65o9I')
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