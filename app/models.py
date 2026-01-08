from sqlalchemy import Column, Integer, String, Enum, Date
from app.database import Base
from app.enums import TaskStatus


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.todo, nullable=False)
    due_date = Column(Date, nullable=True)
