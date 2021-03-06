from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import json_util


MONGODB_URI = "mongodb://<user>:<>@ds137550.mlab.com:37550/student_db"

client = MongoClient(MONGODB_URI) 
db = client.get_database("student_db") #to make client object
student_record = db.student_records

app = Flask(__name__)


@app.route('/')
def index():
	return "Welcome to student records API!"

@app.route("/students/", methods=['GET','POST'])
def student_list():
	if request.method == 'GET':
		students = list(student_record.find())
		return json_util.dumps(students)

	elif request.method == 'POST':
		roll_no = request.form.get("roll_no")

		if student_record.find_one({"roll_no": roll_no}):
			return jsonify({"error":"User already registered"})

		student = {}
		student['roll_no'] = roll_no
		student['name'] = request.form.get("name")
		student['year'] = request.form.get("year")
		student['cgpa'] = request.form.get("cgpa")

		student_record.insert_one(student)

		return jsonify({"result": "Student succcessfuly registered!"})


@app.route('/students/<roll_no>/', methods=['GET','PATCH','DELETE'])
def get_student(roll_no):
	student = student_record.find_one({"roll_no": roll_no})
	if not student:
		return jsonify({"error":"Student not registered"}), 404

	if request.method == 'GET':
		return json_util.dumps(student)

	elif request.method == 'PATCH':
		#student.update(request.form)
		student_record.update_one({'roll_no': roll_no}, {'$set': request.form})
		return jsonify({"result": "record succesfully updated!"})

	elif request.method == 'DELETE':
		student_record.delete_one({'roll_no': roll_no})
		return jsonify({"result": "Student record succesfully deleted!"})




if __name__ == "__main__":
	app.run(port=8000, use_reloader= True, debug=True)


