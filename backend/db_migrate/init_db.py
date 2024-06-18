from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from .app.models import User, Project, Task


engine = create_engine(
    "postgresql://postgres:SanjuMtl06@database-tms.czecim0cqbz3.us-east-2.rds.amazonaws.com/task-management-system"
)
print("Before create database")
print(database_exists(engine.url))

if not database_exists(engine.url):
    create_database(engine.url)

print("After create database")
print(database_exists(engine.url))



try:
    print("Dropping Table: Task")
    Task.__table__.drop(engine)
except Exception as e:
    print(e)


print("Dropping Table: Projects")
Project.__table__.drop(engine)
print("Dropping Table: Users")
User.__table__.drop(engine)

print("Creating Table: Users")
User.__table__.create(engine)
print("Creating Table: Projects")
Project.__table__.create(engine)
print("Creating Table: Task")
Task.__table__.create(engine)
