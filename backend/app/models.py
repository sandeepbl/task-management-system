from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    display_pic_url = Column(String)

    projects_managed = relationship('Project', uselist=False, back_populates='manager')
    tasks_assigned = relationship('Task', back_populates='assignee')

    def __repr__(self):
        return f'User(id:{self.id}, user_name:{self.username})'

    @classmethod
    def get_by_username(cls, username):
        return db.session.query(cls).filter_by(username=username).first()

    @classmethod
    def get_by_id(cls, uid):
        return db.session.query(cls).filter_by(id=uid).first()

    def set_hashed_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String)
    manager_user_id = Column(Integer, ForeignKey('users.id'))

    manager = relationship('User', back_populates='projects_managed')
    tasks = relationship('Task', back_populates='project')

    def __init__(self, title, description, manager_user_id):
        self.title = title
        self.description = description
        self.manager_user_id = manager_user_id

    def __repr__(self):
        return f'Project(id:{self.id}, Name:{self.title})'

    @classmethod
    def get_project_by_id(cls, project_id):
        return db.session.query(cls).filter_by(id=project_id).first()


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String)
    assigned_user_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))

    assignee = relationship('User', back_populates='tasks_assigned')
    project = relationship('Project', back_populates='tasks')

    def __init__(self, title, description, project_id, assigned_user_id):
        self.title = title
        self.description = description
        self.assigned_user_id = assigned_user_id
        self.project_id = project_id

    def __repr__(self):
        return f'Task(id:{self.id}, Name:{self.title})'

    @classmethod
    def get_task_by_title_part(cls, search_text):
        return db.session.query(cls).filter_by(title=search_text).first()


DATABASE_URL = "postgresql+psycopg2://postgres:SanjuMtl06@database-tms" \
               ".czecim0cqbz3.us-east-2.rds.amazonaws.com/task-management-system"

# Creating the PostgreSQL database and tables
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

# Creating a session
Session = sessionmaker(bind=engine)
session = Session()
