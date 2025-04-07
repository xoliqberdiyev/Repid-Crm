from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel, field_validator, Field, model_validator, ValidationError
from utils import security


class EmployeeCreate(BaseModel):
    last_name:str|None=Field(examples=["Kimdir"])
    first_name:str|None=Field(examples=["Nimadir"])
    phone_number:str=Field(examples=["+998949234565"])
    date_of_birth:Optional[datetime|None]=None
    date_of_jobstarted:datetime=Field(examples=['2025-01-01'])
    salary:int = Field(ge=0,examples=[100000])
    username:str=Field(examples=["just_boy"])
    position_id:int=Field(examples=[1])
    password:str=Field(examples=["superhard"])

    @field_validator('phone_number', mode='before')
    @classmethod
    def check_phone_number_validate(cls, phone_number):
        if not security.is_valid_phone_number(phone_number):
            return ValueError('Phone number is not valid form, please be sure')
        return phone_number
    
    @field_validator('password', mode='before')
    @classmethod
    def check_password_validate(cls, password):
        if len(password) < 6:
            return ValueError('Your password must be more than 6 digit')
        return password

    
class ShowEmployee(BaseModel):
    id:int
    last_name: str|None
    first_name: str|None
    phone_number: str
    date_of_birth: Optional[datetime] = None
    date_of_jobstarted: datetime
    username:str
    salary: int
    user_type: str
    image: Optional[str|None] = None
    position:str
    is_active:bool

    model_config = {
        "json_schema_extra": {
            "example": [
            {
                "id":1,
                "last_name": "KImdir",
                "first_name": "Nimadir",
                "phone_number": "+998901234567",
                "date_of_birth": "2000-01-01",
                "date_of_jobstarted": "2024-01-01",
                "salary": 30000,
                "username": "kachokboy",
                "position_id": 1,
                "password": "securepassword",
                "position":True,
                "image":"https://repid-crm.vercel.app/repid.jpg",
                "user_type":"Custom",

            }
            ]
        }
    }

class Token(BaseModel):
    access_token:str
    type:str


class CreateProject(BaseModel):
    name:str
    start_date:datetime
    end_date:datetime
    programmer_ids:List[int]
    price:str

    @field_validator('price',mode='before' )
    @classmethod
    def check_price_validate(cls, price):
        if not price.isdigit():
            return ValueError('Phone number is not valid form, please be sure')
        return price
    
    @model_validator(mode='before')
    @classmethod
    def check_start_end_dates(cls, values):
        start_date = values.get("start_date")
        end_date = values.get("end_date")

        if start_date and end_date and start_date >= end_date:
            raise ValueError('Start date must be less than end date')

        return values



class ProgrammerSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    image: str|None=None

    class Config:
        from_attributes = True
    
        model_config = {
            "json_schema_extra": {
                "example": [
                {
                    'id':1,
                    'first_name':"Shahzod",
                    'last_name':"Abdashev",
                    'image':"https://repid-crm.vercel.app/repid.jpg",
                }
                ]
            }
        }


class ShowProject(BaseModel):
    id: int
    name: str
    start_date: datetime
    end_date: datetime
    image: str
    status:str
    price:str | None
    programmers: List[ProgrammerSchema]

    class Config:
        from_attributes = True

        model_config = {
        "json_schema_extra": {
            "example": [
            {
                "id":1,
                "name": "OnePC",
                "start_date":date(2024,1,1),
                "end_date":date(2024,1,1),
                "image":"Fuck no image",
                "status":"to_do",
                "price":'100000',
                "programmers":{
                    'id':1,
                    'first_name':"Shahzod",
                    'last_name':"Abdashev",
                    'image':"https://repid-crm.vercel.app/repid.jpg",
                }
            }
            ]
        }
    }


    

class UpdateProject(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    programmers: List[int]
    price:str | None

    # @field_validator('price',mode='before' )
    # @classmethod
    # def check_price_validate(cls, price):
    #     if not price.isdigit():
    #         raise ValueError('Phone number is not valid form, please be sure')
    #     return price
    
    # @model_validator(mode='before')
    # @classmethod
    # def check_start_end_dates(cls, values):
    #     start_date = values.get("start_date")
    #     end_date = values.get("end_date")

    #     if start_date and end_date and start_date >= end_date:
    #         raise ValueError('Start date must be less than end date')

    #     return values

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
    projects: List[ShowProject] 

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

    # @model_validator(mode='before')
    # @classmethod
    # def check_start_end_validation(cls, values):
    #     start_date = values.get('start_date')
    #     end_date = values.get('end_date')

    #     if start_date > end_date:
    #         raise ValueError('Start date must be less than end date')
        
    #     return values
    
class ShowNewTask(BaseModel):
    id:int
    name:str
    start_date:datetime
    image_task:str|None
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

    # @model_validator(mode='before')
    # @classmethod
    # def check_start_end_validation(cls, value):
    #     start_date = value.get('start_date')
    #     end_date = value.get('end_date')

    #     if start_date > end_date:
    #         return ValidationError('Please enter valid start and end date')
    #     return value

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
    real_price:str|None=None
    pay_price:str
    type:str
    date_paid:datetime
    description:str
    position:str

    # @model_validator(mode='before')
    # @classmethod
    # def check_price_validation(cls, value):
    #     real_price = value.get('real_price')
    #     pay_price = value.get('pay_price')
    #     if not real_price.isdigit() or not pay_price.isdigit():
    #         return 'Please enter valid int for price field'
    #     elif real_price == None:
    #         pass
    #     return value

class CreateIncomeProject(BaseModel):
    pay_price:str
    project_id:int
    description:str
    date_paid:datetime
    
class ShowIncomeStudent(BaseModel):
    id:int
    name:str
    real_price:str|None=None
    pay_price:str
    left_price:int
    description:str|None=None
    date_paied:datetime
    position:str
    type:str

class ShowIncomeProject(BaseModel):
    id:int
    name:str
    project_id:int
    date_start:datetime
    date_end:datetime
    description:str|None=None
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
    description:str = None
    date_paied:datetime= None
    position:str= None
    

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
    password:Optional[str]=None
    is_active:bool

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
    from_whom:str
    type:str

    model_config = {
        "json_schema_extra": {
            "example": 
            {
                "name":"Komputer",
                "price_paid":"100000",
                "description":"Someting",
                "date_paied":date(2024,1,1),
                'from_whom':"oybek",
                "type":"for_office"
                }
        }
    }

class ShowExpenseType(BaseModel):
    id:int
    name:str
    price_paid:str
    description:str
    date_paied:datetime
    real_price:str|None
    from_whom:str|None
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
    date_paid:datetime

    # @field_validator('price_paied', mode='before')
    # @classmethod
    # def check_price_validation(cls,price_paied):
    #     if not price_paied.isdigit():
    #         raise ValueError('Price must be as int, enter valid one')
    #     return price_paied

class ShowExpenseEmployee(BaseModel):
    id:int
    pay_paied:str
    user_id:int
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
    type:str
    from_whom:str|None = None

    # @field_validator('price_paid', mode='before')
    # @classmethod
    # def check_price_validation(cls, price_paid):
    #     if price_paid is None:
    #         pass
    #     elif price_paid.isdigit():
    #         raise ValueError('Price must be as integer')
    #     return price_paid

class BaseFilterProject(BaseModel):
    start_date:datetime=None
    end_date:datetime=None
    status:str=None

class ShowLoginPassword(BaseModel):
    id:int
    name:str
    login:str
    password:str

class UpdateLoginPassword(BaseModel):
    name:str|None=None
    login:str|None = None
    password:str|None = None

class UpdateExpenseSalary(BaseModel):
    price_paid:str|None=None
    user_id:int|None=None
    date_paid:datetime|None=None

    # @field_validator('price_paid', mode='before')
    # @classmethod
    # def check_price_validation(cls, price_paid):
    #     if price_paid is None:
    #         pass
    #     elif price_paid.isdigit():
    #         raise ValueError('Price must be as integer')
    #     return price_paid
    
class UpdateIncomeProject(BaseModel):
    pay_price:str|None=None
    project_id:int|None=None
    description:str|None=None
    date_paid:datetime|None=None

    # @field_validator('pay_price', mode='before')
    # @classmethod
    # def check_price_validation(cls, pay_price):
    #     if pay_price is None:
    #         pass
    #     elif pay_price.isdigit():
    #         raise ValueError('Price must be as integer')
    #     return pay_price