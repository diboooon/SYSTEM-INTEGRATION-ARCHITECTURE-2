
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI()

# Data model using Pydantic
class EmployeeCreate(BaseModel):
    name: str
    position: str
    department: str

class Employee(EmployeeCreate):
    id: int

# Database connection setup
def create_connection():
    connection = sqlite3.connect("employees.db")
    return connection

# Create table if not exists
def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT NOT NULL,
        department TEXT NOT NULL
    )
    """)
    connection.commit()
    connection.close()

create_table()

# CRUD functions
def create_employee(employee: EmployeeCreate):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO employees (name, position, department) VALUES (?, ?, ?)", (employee.name, employee.position, employee.department))
    connection.commit()
    employee_id = cursor.lastrowid
    connection.close()
    return employee_id

def read_employees():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    connection.close()
    return [Employee(id=row[0], name=row[1], position=row[2], department=row[3]) for row in employees]

def read_employee(employee_id: int):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employees WHERE id=?", (employee_id,))
    employee = cursor.fetchone()
    connection.close()
    if employee:
        return Employee(id=employee[0], name=employee[1], position=employee[2], department=employee[3])
    raise HTTPException(status_code=404, detail="Employee not found")

def update_employee(employee_id: int, updated_employee: EmployeeCreate):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE employees SET name=?, position=?, department=? WHERE id=?", (updated_employee.name, updated_employee.position, updated_employee.department, employee_id))
    connection.commit()
    connection.close()
    return {"message": "Employee updated successfully"}

def delete_employee(employee_id: int):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))
    connection.commit()
    connection.close()
    return {"message": "Employee deleted successfully"}

# FastAPI endpoints
@app.post("/employees/", response_model=Employee)
def create_employee_endpoint(employee: EmployeeCreate):
    employee_id = create_employee(employee)
    return {"id": employee_id, **employee.dict()}

@app.get("/employees/", response_model=List[Employee])
def read_employees_endpoint():
    return read_employees()

@app.get("/employees/{employee_id}", response_model=Employee)
def read_employee_endpoint(employee_id: int):
    return read_employee(employee_id)

@app.put("/employees/{employee_id}")
def update_employee_endpoint(employee_id: int, updated_employee: EmployeeCreate):
    return update_employee(employee_id, updated_employee)

@app.delete("/employees/{employee_id}")
def delete_employee_endpoint(employee_id: int):
    return delete_employee(employee_id)
