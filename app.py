from flask import *
import random
import hashlib
import mysql.connector

app = Flask(__name__)
con = mysql.connector.connect(host='remotemysql.com',database='cVLw2NAjNX',user='cVLw2NAjNX',password='7I3RP65o9I')

@app.route('/generatetoken',methods=['GET'])
def generateToken():
    cursor = con.cursor()
    query = "Insert into tokens (client_id, token) values (%s,%s)"
    k = random.randint(0,199999)
    s = str(k)
    token = hashlib.sha224(s.encode()).hexdigest()
    data = (request.args.get('id'),token)
    cursor.execute(query, data)
    con.commit()
    cursor.close()
    print(token)
    return token
@app.route('/createclient',methods=['GET'])
def createClient():
    cursor = con.cursor()
    query = "Insert into tokens (emp_id, client_id) values (%s,%s)"
    k = random.randint(0,19999)
    s = str(k)
    client = hashlib.sha256(s.encode()).hexdigest()
    data = (request.args.get('id'),client)
    cursor.execute(query, data)
    con.commit()
    cursor.close()
    return client    

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8090,debug=False)