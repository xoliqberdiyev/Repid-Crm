from datetime import datetime
from typing import Optional, List,Generic, TypeVar

from pydantic import BaseModel, constr, field_validator, Field


class EmployeeCreate(BaseModel):
    last_name:str
    first_name:str
    phone_number:str
    date_of_birth:Optional[datetime|None]=None
    date_of_jobstarted:datetime
    salary:int
    username:str
    position_id:int
    password:str

    class Config:
        orm_format = True

    # @field_validator('date_of_birth', 'date_of_jobstarted')
    # def make_datetimes_naive(cls, v):
    #     if cls.tzinfo is not None:
    #         v = v.replace(tzinfo=None)
    #     return v
    
class ShowEmployee(BaseModel):
    id:int
    last_name: str
    first_name: str
    phone_number: str
    date_of_birth: Optional[datetime] = None
    date_of_jobstarted: datetime
    username:str
    salary: int
    user_type: str
    image: Optional[str|None] = None
    position:str

    class Config:
        orm_format = True

class Token(BaseModel):
    access_token:str
    type:str


class CreateProject(BaseModel):
    name:str
    start_date:datetime
    end_date:datetime
    programmer_ids:List[int]
    price:str


class ProgrammerSchema(BaseModel):
    id: int
    first_name: str
    image: str|None
    last_name: str

    class Config:
        from_attributes = True


class ShowProject(BaseModel):
    id: int
    name: str
    start_date: datetime
    end_date: datetime
    image: str
    programmers: List[ProgrammerSchema]
    status:str
    price:str | None

    class Config:
        from_attributes = True

class UpdateProject(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    programmers: List[int]
    price:str | None

    class Config:
        from_attributes = True

class ShowEmployeeDetail(BaseModel):
    id:int
    last_name: str
    first_name: str
    phone_number: str
    position_id:int
    position_name:str
    date_of_birth: Optional[datetime] = None
    date_of_jobstarted: datetime
    username:str
    salary: int
    user_type: str
    image: Optional[str] = None
    projects: List[ShowProject] = []

    class Config:
        from_attributes = True


class CreateOperator(BaseModel):
    full_name:str
    phone_number:str
    description:str
    operator_type_id:int


class ShowOperator(BaseModel):
    id:int
    full_name:str
    phone_number:str
    description:str
    operator_type_id:int
    operator_type:Optional[str]
    status:str

    class Config:
        from_attributes = True

class ShowExpectedValue(BaseModel):
    id:int
    name:str
    date:Optional[datetime|None] = None
    description:str
    type:Optional[str] = None
    price:int

    class Config:
        from_attributes = True

class CreateExpectedValue(BaseModel):
    name:str
    date:Optional[datetime|None] = None
    description:str
    type:str
    price:int

class UpdateExpectedValue(BaseModel):
    name:Optional[str] = None
    date:Optional[datetime] = None
    description:Optional[str] =None
    price:Optional[int]=None
    

class CreateNewTask(BaseModel):
    name:str
    start_date:datetime
    end_date:datetime
    programmer_ids:List[int]
    description:str
    status:str

class ShowNewTask(BaseModel):
    id:int
    name:str
    start_date:datetime
    end_date:datetime
    programmer_ids:List[ProgrammerSchema]
    description:str
    status:str

class UpdateNewTask(BaseModel):
    name: Optional[str] = None
    start_date:Optional[datetime] = None
    end_date:Optional[datetime] = None
    programmer_ids:List[int]
    description:Optional[str] = None

class ShowPosition(BaseModel):
    id:int
    name:str

class ShowCurrentUser(BaseModel):
    id:int
    last_name:str
    first_name:str
    image:str
    user_type:str
    
class CreateIncomeStudent(BaseModel):
    name:str
    real_price:str
    pay_price:str
    date_paid:datetime
    position:str


class CreateIncomeProject(BaseModel):
    pay_price:str
    project_id:int
    
class ShowIncomeStudent(BaseModel):
    id:int
    name:str
    real_price:str
    pay_price:str
    left_price:int
    date_paied:datetime
    position:str
    type:str

class ShowIncomeProject(BaseModel):
    id:int
    name:str
    date_start:datetime
    date_end:datetime
    real_price:str
    pay_price:str
    left_price:int
    date_paied:datetime
    type:str
    programmers:List[ProgrammerSchema]

class UpdateStudentIncome(BaseModel):
    name:str = None
    real_price:str= None
    pay_price:str= None
    date_paied:datetime= None
    position:str= None
    
class UpdateIncomeProject(BaseModel):
    pay_price:str

class UpdateEmployeeDetail(BaseModel):
    name:Optional[str]=None
    date_of_birth:Optional[datetime]=None
    salary:Optional[int]=None
    last_name:Optional[str]=None
    username:Optional[str]=None
    first_name:Optional[str]=None
    phone_number:Optional[str]=None
    date_of_jobstarted:Optional[datetime]=None
    position_id:Optional[int]=None

class UpdateOperator(BaseModel):
    full_name:str=None
    phone_number:str=None
    description:str=None

class CreateNewExpence(BaseModel):
    name:str
    price_paid:str
    real_price:Optional[str|None]=None
    description:str
    date_paied:datetime
    type:str

class ShowExpenseType(BaseModel):
    id:int
    name:str
    price_paid:str
    description:str
    date_paied:datetime
    real_price:str|None
    remainder_price:int|None
    type:str

class CreateExpenseUser(BaseModel):
    user_id:int
    paid_price:str

class ShowExepnseUser(BaseModel):
    first_name:str
    last_name:str
    phone_number:str
    position:str
    job_started:datetime
    salary:int
    date_paid:datetime
    price_paid:datetime
    remainder_price:str

class CreatingExepnseEmployee(BaseModel):
    employee_id:int
    price_paied:str

class ShowExpenseEmployee(BaseModel):
    id:int
    pay_paied:str
    remainder_price:int
    date_last_paied:datetime
    first_name:str
    last_name:str
    position_name:str
    start_of_job:datetime
    salary:int
    phone_number:str
    img:str|None

class UpdateExpenseByType(BaseModel):
    name:Optional[str|None]=None
    price_paid:Optional[str|None] = None
    description:Optional[str|None] = None
    date_paied:Optional[datetime|None] = None
    real_price:Optional[str|None] = None

class BaseFilterProject(BaseModel):
    start_date:datetime=None
    end_date:datetime=None
    status:str=None

class ShowLoginPassword(BaseModel):
    id:int
    login:str
    password:str

class UpdateLoginPassword(BaseModel):
    login:str|None = None
    password:str|None = None