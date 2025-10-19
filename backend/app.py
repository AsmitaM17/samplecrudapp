from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# MySQL configurations
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'student_db')

mysql = MySQL(app)

@app.route('/api/students', methods=['GET'])
def get_students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    cur.close()
    return jsonify([{
        'id': student[0],
        'name': student[1],
        'email': student[2],
        'course': student[3]
    } for student in students])

@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO students (name, email, course) VALUES (%s, %s, %s)",
        (data['name'], data['email'], data['course'])
    )
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Student added successfully'}), 201

@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE students SET name=%s, email=%s, course=%s WHERE id=%s",
        (data['name'], data['email'], data['course'], id)
    )
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Student updated successfully'})

@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Student deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)