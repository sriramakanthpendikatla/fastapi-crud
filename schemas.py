from pydantic import BaseModel


class Studentcreate(BaseModel):
    name: str
    age: int
    course: str


class Student(Studentcreate):
    id: int

    class Config:
        orm_mode = True