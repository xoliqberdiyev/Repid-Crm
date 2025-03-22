import datetime
import enum
import os

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum, String, ForeignKey, INTEGER, Boolean
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import BigInteger


class Base(DeclarativeBase):
    pass

class UserType(str, enum.Enum):
    super_admin = 'Super admin'
    admin = 'Admin'
    custom = 'Custom'

class StatusProject(str, enum.Enum):
    in_progres = 'in_progres'
    done = 'done'
    cancel = 'cancel'

class StatusOperator(str, enum.Enum):
    empty = '--'
    in_progres = 'in_progres'
    done = 'done'
    cancel = 'cancel'

class StatusTask(str, enum.Enum):
    to_do = 'to_do'
    in_progres = 'in_progres'
    done = 'done'
    code_review = 'code_review'
    success = 'success'

class StatusExpectedVAlue(str, enum.Enum):
    income = 'income'
    expense = 'expense'

class ExpenseType(str, enum.Enum):
    employee_salary='employee_salary'
    for_office='for_office'
    smm_service='smm_service'
    renting='renting'
    other_expense='other_expense'
    office_item = 'office_item'
    tax = 'tax'

class ExpenseFromWhom(str, enum.Enum):
    oybek='oybek'
    bahrom='bahrom'
    income='income'

class IncomeType(str, enum.Enum):
    from_student = 'from_student'
    from_project='from_project'
    investor='investor'

class ProjectProgrammer(Base):
    __tablename__ = 'project_programmer'

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id:Mapped[int] = mapped_column(ForeignKey('projects.id',ondelete='CASCADE'))
    programmer_id: Mapped[int] = mapped_column(ForeignKey('employees.id',ondelete='CASCADE'))


class TaskProgrammer(Base):
    __tablename__ = 'task_programmer'

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id:Mapped[int] = mapped_column(ForeignKey('tasks.id'))
    programmer_id: Mapped[int] = mapped_column(ForeignKey('employees.id'))


class Employees(Base):
    __tablename__ = 'employees'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str|None] = mapped_column(String(100), default=None)
    username: Mapped[str] = mapped_column(String(100),unique=True)
    last_name: Mapped[str|None] = mapped_column(String(100), default=None)
    phone_number: Mapped[str|None] = mapped_column(String(50), default=None)
    date_of_birth: Mapped[datetime.datetime | None]
    date_of_jobstarted: Mapped[datetime.datetime | None]
    position_id: Mapped[int|None] = mapped_column(ForeignKey('positions.id',ondelete='CASCADE'))
    image: Mapped[str | None] = mapped_column(String,index=True)
    salary: Mapped[int | None] = mapped_column(BigInteger)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType), default=UserType.custom)
    password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_time: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())

    projects = relationship(
        "Project",
        secondary="project_programmer",
        back_populates="programmers",
        cascade="all, delete"
    )

    tasks = relationship(
        "Task",
        secondary="task_programmer",
        back_populates="programmers",
        cascade="all, delete"
    )

    position: Mapped['Position'] = relationship(back_populates='user')
    expense:Mapped['ExpenseData'] = relationship(back_populates='employee_salary')

    def __repr__(self) -> str:
        return f"Employees(id={self.id!r}, last_name={self.last_name!r})"


class Position(Base):
    __tablename__ = 'positions'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    user: Mapped['Employees'] = relationship(back_populates='position')

    def __repr__(self) -> str:
        return f"Positions(id={self.id!r}, name={self.name!r})"


class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    start_date: Mapped[datetime.datetime | None]
    end_date: Mapped[datetime.datetime | None]
    status: Mapped[StatusProject] = mapped_column(Enum(StatusProject), default=StatusProject.in_progres)
    image: Mapped[str] = mapped_column(String,index=True)
    price: Mapped[str] = mapped_column(String, nullable=True)
    is_deleted:Mapped[bool|None] = mapped_column(Boolean, nullable=True ,default=False)

    programmers = relationship(
        "Employees",
        secondary="project_programmer",
        back_populates="projects",
        cascade="all, delete"
    )
    income_data:Mapped['IncomeData'] = relationship(back_populates='project',cascade="all, delete")


class Operator(Base):
    __tablename__='operators'

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(100))
    description: Mapped[str]
    status:Mapped[StatusOperator] = mapped_column(Enum(StatusOperator), default=StatusOperator.empty)
    operator_type_id: Mapped[int] = mapped_column(ForeignKey('operator_type.id', ondelete='CASCADE'))

    operator_type: Mapped['OperatorType'] = relationship(back_populates='operator')


class OperatorType(Base):
    __tablename__='operator_type'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    operator: Mapped[Operator] = relationship(back_populates='operator_type')


class ExcpectedValue(Base):
    __tablename__ = 'expected_value'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(String(100))
    date: Mapped[datetime.datetime|None]
    price:Mapped[int] = mapped_column(BigInteger)
    description: Mapped[str]
    type: Mapped[StatusExpectedVAlue] = mapped_column(Enum(StatusExpectedVAlue))


class Task(Base):
    __tablename__ ='tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(String(100))
    start_date: Mapped[datetime.datetime]
    end_date: Mapped[datetime.datetime]
    image_task:Mapped[str|None] = mapped_column(String(100),default=None)
    status: Mapped[StatusTask] = mapped_column(Enum(StatusTask), default=StatusTask.to_do)
    is_deleted:Mapped[bool|None] = mapped_column(Boolean, nullable=True ,default=False)
    description: Mapped[str]

    programmers = relationship(
        "Employees",
        secondary="task_programmer",
        back_populates="tasks",
        cascade="all, delete"
    )

class IncomeData(Base):
    __tablename__ = 'incomes'

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[int|None] = mapped_column(String(100), default=None)
    real_price: Mapped[str|None] = mapped_column(String(100),default=None)
    pay_price:Mapped[str|None] = mapped_column(String(100))
    description:Mapped[str|None] = mapped_column(default=None)
    date_paied:Mapped[datetime.datetime|None] = mapped_column(
         default=datetime.datetime.now
    )
    position:Mapped[str|None] = mapped_column(default=None)
    project_id:Mapped[int|None] = mapped_column(ForeignKey('projects.id',ondelete='CASCADE'),default=None)
    type:Mapped[IncomeType] = mapped_column(Enum(IncomeType))

    project:Mapped['Project'] = relationship(back_populates='income_data',cascade="all, delete")


class ExpenseData(Base):
    __tablename__ = 'expences'

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str|None] = mapped_column(default=None)
    real_price:Mapped[str|None] = mapped_column(default=None)
    price_paid:Mapped[str] = mapped_column(String(100))
    description:Mapped[str|None] = mapped_column(default=None)
    date_paied:Mapped[datetime.datetime] = mapped_column(
         default=datetime.datetime.now
    )
    from_whom:Mapped[ExpenseFromWhom|None] = mapped_column(Enum(ExpenseFromWhom), default=None)
    employee_salary_id:Mapped[int|None] = mapped_column(ForeignKey('employees.id',ondelete='CASCADE'))
    type:Mapped[ExpenseType] = mapped_column(Enum(ExpenseType))

    employee_salary:Mapped['Employees'] = relationship(back_populates='expense')


class LoginPasswordNote(Base):
    __tablename__ = 'login_pass_note'

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(150))
    login:Mapped[str] = mapped_column(String(100))
    password:Mapped[str] = mapped_column(String(100))

    




