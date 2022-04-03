import mysql.connector
import time
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
while True:
    try:
        mydb = mysql.connector.connect(
        host="rest_db_1",
        user="root",
        password="root",
        port= '3306',
        database = "students"
        )
        print("Connected")
        break
    except Exception as e:
        print(f"Excetion {e}")
        print("Failed connection, trying again")

mycursor = mydb.cursor()
class student_db:
    def get_student(self, student_id):
        mycursor.execute(f"SELECT * FROM student WHERE ID='{student_id}';")
        myresult = mycursor.fetchall()
        return myresult

    def all_get_students(self):
        mycursor.execute("SELECT * FROM student;")
        myresult = mycursor.fetchall()
        return myresult 

    def update_student(self, student_id):
        parser.add_argument("name")
        parser.add_argument("age")
        parser.add_argument("spec")
        args = parser.parse_args()
        mycursor.execute(f"SELECT * FROM student WHERE ID='{student_id}';")
        myresult = mycursor.fetchall()
        name = myresult[0][1]
        age = myresult[0][2]
        spec = myresult[0][3]
        if(args["name"] is not None):
            name = args["name"]
        if(args["age"] is not None):
            age  = args["age"]
        if(args["spec"] is not None):
            spec = args["spec"]
        mycursor.execute(f"UPDATE student SET name = '{name}', age = '{age}', spec = '{spec}' WHERE ID = '{student_id}';")
        mydb.commit()
        # return True

    def put_student(self): # insert
        parser.add_argument("name")
        parser.add_argument("age")
        parser.add_argument("spec")
        args = parser.parse_args()
        name = args["name"]
        age = args["age"]
        spec = args["spec"]
        mycursor.execute(f"SELECT MAX(ID) FROM student;") 
        my_result = mycursor.fetchall()
        if my_result and my_result[0][0]:
            student_id = my_result[0][0] + 1
        else:
            student_id = 1
        if((args["name"] is not None) and (args["age"] is not None) and (args["spec"] is not None)):
            mycursor.execute(f"INSERT INTO student (ID, Name, Age, Spec) VALUES ('{student_id}', '{name}', '{age}', '{spec}');")
            mydb.commit()
            return True
        else:
            return False
    
    def delete_student(self,student_id):
        parser.add_argument("name")
        parser.add_argument("age")
        parser.add_argument("spec")
        args = parser.parse_args()
        mycursor.execute(f"DELETE FROM student WHERE ID = '{student_id}';")
        mydb.commit()


class StudentsList(Resource):

    def get(self,student_id):
        x = student_db()
        return x.all_get_students()
  
    def put(self,student_id):
        x = student_db()
        if(x.put_student()):
            return 201
        else:
            return 404
    
    def post(self,student_id):
        x = student_db()
        x.update_student(student_id)

    def delete(self,student_id):
        x = student_db()
        x.delete_student(student_id)



api.add_resource(StudentsList, '/students1/<student_id>')
if __name__ == "__main__":
  app.run(debug=True,host='0.0.0.0')
