from fastapi import FastAPI
import json

app = FastAPI()

# Safe loading of JSON
try:
    with open('./data.json') as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = []

@app.get('/')
def hello_world():
    if not data:
        return {"message": "Hello! No students found."}
    student_names = [student.get("name", "Unknown") for student in data[:3]]
    return {
        "message": "Hello! Welcome to the student API.",
        "total_students": len(data),
        "some_students": student_names
    }

@app.get('/students')
def get_students(pref: str = None):
    if pref:
        return [student for student in data if student.get("pref") == pref]
    return data

@app.get('/students/{student_id}')
def get_student(student_id: int):
    for student in data:
        if student.get("id") == student_id:
            return student
    return {"error": "Student not found"}

@app.get('/stats')
def get_stats():
    counts = {}
    for student in data:
        p = student.get("pref", "Unknown")
        counts[p] = counts.get(p, 0) + 1
    return counts

@app.get('/add/{x}/{y}')
def add(x: int, y: int):
    return {"result": x + y}

@app.get('/subtract/{x}/{y}')
def subtract(x: int, y: int):
    return {"result": x - y}
