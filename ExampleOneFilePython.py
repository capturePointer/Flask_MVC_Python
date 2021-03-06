import os
from pprint import pprint

from flask import Flask
from flask import json
from flask import render_template
from flask import request
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash

project_root = os.path.dirname(__name__)
template_path = os.path.join(project_root)

app = Flask(__name__,template_folder=template_path)
# mysql configuratoin
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']       = 'localhost'
app.config['MYSQL_DATABASE_USER']       = 'root'
app.config['MYSQL_DATABASE_PASSWORD']   = ''
app.config['MYSQL_DATABASE_DB']         = 'test'
mysql.init_app(app)

@app.route('/')
def main_world():
    return render_template('static/index.html')

@app.route('/signup',methods=['POST'])
def signUp():
    # open connection

    # read request from UI
    _name   = request.form['name']
    _email  = request.form['email']
    _pass   = request.form['pass']
    _hash_pass = generate_password_hash(_pass)

    if _name and _email and _pass:
        insert(_name,_email,_hash_pass)
        return json.dumps({'html':'<span>Data Inserted </span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

def insert(user,email,password):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO user (
                username,
                email,
                password
            ) 
            VALUES (%s,%s,%s)""",(user,email,password))
    conn.commit()
    conn.close()

@app.route('/show')
def show():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user")
    data = cursor.fetchall()
    dataList = []
    if data is not None:
        for item in data:
            dataTempObj = {
                'id'        : item[0],
                'name'      : item[1],
                'email'     : item[2],
                'password'  : item[3]
            }
            dataList.append(dataTempObj)
        return json.dumps(dataList)
    else:
        return 'data kosong'

@app.route('/update/<id>',methods=['POST'])
def update(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("UPDATE user SET username = %s, email = %s, password = %s WHERE id = %s",(request.form['username'],request.form['email'],request.form['password'],int(id)))
    conn.commit()
    conn.close()
    if(result):
        return json.dumps({'updated':'true'})
    else:
        return json.dumps({'updated':'false'})

@app.route('/delete/<id>')
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("DELETE FROM user WHERE id = %s",int(id))
    conn.commit()
    conn.close()
    if(result):
        return json.dumps({'delete':'true'})
    else:
        return json.dumps({'delete':'false'})

if __name__ == '__main__':
    app.run()