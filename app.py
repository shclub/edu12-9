#!/usr/bin/python
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys

def handler(event, context):
    return 'Hello from AWS Lambda using Python' + sys.version + '!'        

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
# app.config.from_pyfile('config.py')

def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn

def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''DROP TABLE employee''')
        conn.execute('''
            CREATE TABLE employee (
                id INTEGER PRIMARY KEY NOT NULL,
                empName TEXT NOT NULL,
                empDeptName TEXT,
                empTelNo TEXT,
                empMail TEXT
            );
        ''')

        conn.commit()
        print("employee table created successfully")
    except:
        print("employee table creation failed - Maybe table")
    finally:
        conn.close()


def insert_employee(employee):
    inserted_employee = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO employee (empName, empDeptName, empTelNo, empMail) VALUES (?, ?, ?, ?, ?)", (employee['empName'], employee['empDeptName'], employee['empTelNo'], employee['empMail']) )
        conn.commit()
        inserted_employee = get_employee_by_id(cur.lastrowid)
    except:
        conn().rollback()
    finally:
        conn.close()
    return inserted_employee


def get_employees():
    employees = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM employee")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            employee = {}
            employee["id"] = i["id"]
            employee["empName"] = i["empName"]
            employee["empDeptName"] = i["empDeptName"]
            employee["empTelNo"] = i["empTelNo"]
            employee["empMail"] = i["empMail"]
            employees.append(employee)
    except:
        employees = []
    return employees


def get_employee_by_id(id):
    employee = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM employee WHERE id = ?", (id,))
        row = cur.fetchone()

        # convert row object to dictionary
        employee["id"] = row["id"]
        employee["empName"] = row["empName"]
        employee["empDeptName"] = row["empDeptName"]
        employee["empTelNo"] = row["empTelNo"]
        employee["empMail"] = row["empMail"]
    except:
        employee = {}
    return employee


def update_employee(employee):
    updated_employee = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE employee SET empName = ?, empDeptName = ?, empTelNo = ?, empMail = ? WHERE id =?", (employee["empName"], employee["empDeptName"], employee["empTelNo"], employee["empMail"], employee["id"],))
        conn.commit()
        #return the employee
        updated_employee = get_employee_by_id(employee["id"])
    except:
        conn.rollback()
        updated_employee = {}
    finally:
        conn.close()
    return updated_employee


def delete_employee(id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from employee WHERE id = ?", (id))
        conn.commit()
        message["status"] = "employee deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete employee"
    finally:
        conn.close()
    return message


employees = []
employee0 = {
    "name": "Charles Effiong",
    "email": "charles@gamil.com",
    "phone": "067765665656",
    "address": "Lui Str, Innsbruck"
}

employee1 = {
    "name": "Sam Adebanjo",
    "email": "samadebanjo@gamil.com",
    "phone": "098765465",
    "address": "Sam Str, Vienna"
}  

employees.append(employee0)
employees.append(employee1)

create_db_table()

#for i in employees:
#    print(insert_employee(i))

@app.route("/")
def template_test():
    return render_template(
                'index.html',                      #렌더링 html 파일명
                title="Flask Template Test",       #title 텍스트 바인딩1
                my_str="Hello Flask!",             #my_str 텍스트 바인딩2
                my_list=[x + 1 for x in range(10)] #30개 리스트 선언(1~30)
            )
  

@app.route('/api/v1/employees', methods=['GET'])
def api_get_employees():
    return jsonify(get_employees())

@app.route('/api/v1/employees/<id>', methods=['GET'])
def api_get_employee(id):
    return jsonify(get_employee_by_id(id))

@app.route('/api/v1/employees',  methods = ['POST'])
def api_add_employee():
    employees = request.get_json()
    return jsonify(insert_employee(employees))

@app.route('/api/v1/employees/<id>',  methods = ['POST'])
def api_update_employee():
    employees = request.get_json()
    return jsonify(update_employee(id,employees))

@app.route('/api/v1/employee/<id>',  methods = ['POST'])
def api_delete_employee(id):
    return jsonify(delete_employee(id))

# health_check
@app.route('/health_check', methods = ['GET'])
def health_check():
    if request.method == 'GET':
        return json.dumps({'returnCode': 'OK'})
    else:
        return json.dumps({'returnCode': 'NG', 'message': 'Method ' + request.method + ' not allowed.'}, status=405)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    #app.run(host='0.0.0.0',port=8000,debug=True)
