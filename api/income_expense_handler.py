from datetime import datetime

from fastapi import APIRouter, Depends
from typing import List, Optional
from fastapi_pagination.utils import disable_installed_extensions_check

from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession
from database import schemas, session, models
from api.action import income_expense
from api.login_handler import get_current_user_from_token

expense_income_handler = APIRouter()

@expense_income_handler.post('/create_income_student')
async def create_income_student(body:schemas.CreateIncomeStudent ,db:AsyncSession = Depends(session.get_db),
                                current_user:models.Employees=Depends(get_current_user_from_token)):
    return await income_expense._create_income_student(body=body, session=db)

@expense_income_handler.get('/list-income-student', response_model=Page[schemas.ShowIncomeStudent])
async def get_list_income_student(db:AsyncSession=Depends(session.get_db),
                                  start_date:datetime|None=None,
                                  end_date:datetime|None=None,
                                  current_user:models.Employees=Depends(get_current_user_from_token)):
    income_students = await income_expense._get_list_income_student(session=db,start_date=start_date,end_date=end_date)
    disable_installed_extensions_check()
    return paginate(income_students)

@expense_income_handler.delete('/delete-income-student')
async def delete_create_income(income_student_id:int, db:AsyncSession=Depends(session.get_db),
                               current_user:models.Employees=Depends(get_current_user_from_token)):
    return await income_expense._delete_income_student(income_student_id=income_student_id, session=db)

@expense_income_handler.patch('/update-income-student')
async def update_income_student(income_student_id:int, update_params:schemas.UpdateStudentIncome, db:AsyncSession=Depends(session.get_db),
                                current_user:models.Employees=Depends(get_current_user_from_token)):
    body = update_params.model_dump(exclude_none=True)
    return await income_expense._update_income_student(session=db, income_student_id=income_student_id,
                                                       body=body)

@expense_income_handler.post('/create_income_project')
async def create_income_project(body:schemas.CreateIncomeProject, db:AsyncSession=Depends(session.get_db),
                                current_user:models.Employees=Depends(get_current_user_from_token)):
    return await income_expense._create_income_project(session=db, body=body)

@expense_income_handler.get('/get-list-income-project', response_model=Page[schemas.ShowIncomeProject])
async def get_list_income_project(db:AsyncSession=Depends(session.get_db),
                                  start_date:datetime|None=None,
                                  end_date:datetime|None=None,
                                  current_user:models.Employees=Depends(get_current_user_from_token)):
    income_projects = await income_expense._get_list_income_project(session=db,start_date=start_date,end_date=end_date)
    return paginate(income_projects)

@expense_income_handler.delete('/delete-income-project')
async def delete_income_project(income_project_id:int, db:AsyncSession=Depends(session.get_db),
                                current_user:models.Employees=Depends(get_current_user_from_token)):
    return await income_expense._delete_income_project(income_project_id=income_project_id,
                                                       session=db)

@expense_income_handler.patch('/update-income-project')
async def update_income_project(income_project_id:int,update_params:schemas.UpdateIncomeProject,session:AsyncSession=Depends(session.get_db),
                                current_user:models.Employees=Depends(get_current_user_from_token)):
    body = update_params.model_dump()
    return await income_expense._update_income_project(body=body,
                                                       session=session,
                                                       income_project_id=income_project_id)

@expense_income_handler.get('/get-pie-chart-income')
async def get_income_chiechart(db:AsyncSession=Depends(session.get_db),
                                current_user:models.Employees=Depends(get_current_user_from_token)):
    return await income_expense._get_income_piechart(session=db)

@expense_income_handler.post('/create-expense-type',
                             description="Bu yerda shu status lar keladi (for_office, smm_service, other_expense, renting)")
async def create_expense(body:schemas.CreateNewExpence,db:AsyncSession=Depends(session.get_db),
                          current_user:models.Employees=Depends(get_current_user_from_token)):
    return await income_expense._create_expence_type(session=db, body=body)

@expense_income_handler.patch('/update-expense',response_model=schemas.ShowExpenseType)
async def update_expense(update_params:schemas.UpdateExpenseByType, expense_id:int ,db:AsyncSession=Depends(session.get_db),
                          current_user:models.Employees=Depends(get_current_user_from_token)):
    body = update_params.model_dump(exclude_none=True)
    return await income_expense._update_expense_by_type(body=body, session=db, expense_id=expense_id)

@expense_income_handler.get('/list-expense-type', response_model = Page[schemas.ShowExpenseType],
                            description="Bu yerda shu status lar keladi (for_office, smm_service, other_expense,renting)")
async def get_list_expense_type(type:str, db:AsyncSession=Depends(session.get_db),
                                start_date:datetime|None=None,
                                end_date:datetime|None=None,
                                 current_user:models.Employees=Depends(get_current_user_from_token)):
    expesne_types = await income_expense._get_expence_type_list(session=db, status=type,
                                                                start_date=start_date,end_date=end_date)
    return paginate(expesne_types)

@expense_income_handler.delete('/delete-expense')
async def delete_given_expense(expense_id:int, db:AsyncSession=Depends(session.get_db),
                                current_user:models.Employees=Depends(get_current_user_from_token)):
    return await income_expense._delete_expense(session=db,expense_id=expense_id)

@expense_income_handler.post('/create-expense-salary-employee',
                            description="Bu yerda faqat employee_id orqali user expense chiqadi")
async def create_expense_employee(body:schemas.CreatingExepnseEmployee, db:AsyncSession=Depends(session.get_db),
                                   current_user:models.Employees=Depends(get_current_user_from_token)):
    return await income_expense._create_expense_employee(session=db, body=body)

@expense_income_handler.get('/list-expense-employee', response_model=Page[schemas.ShowExpenseEmployee])
async def get_list_expense_employee(db:AsyncSession=Depends(session.get_db),
                                    start_date:datetime|None=None,
                                    end_date:datetime|None=None,
                                     current_user:models.Employees=Depends(get_current_user_from_token)):
    user_expences = await income_expense._list_expense_employee(session=db, start_date=start_date, end_date=end_date)
    return paginate(user_expences)

@expense_income_handler.patch('/update-expense-salary-employee')
async def update_expense_employee(income_employee_id:int,update_params: schemas.UpdateExpenseSalary,db:AsyncSession=Depends(session.get_db),
                                   current_user:models.Employees=Depends(get_current_user_from_token)):
    body = update_params.model_dump()
    return await income_expense._update_expense_employee(session=db, body=body,income_employee_id=income_employee_id)

@expense_income_handler.get('/get-expense-pie-chart')
async def get_expense_pie_chart(db:AsyncSession=Depends(session.get_db),
                                 current_user:models.Employees=Depends(get_current_user_from_token)):
    return await income_expense._expense_pie_chart(session=db)

@expense_income_handler.get('/get-line-graph-month-expense')
async def get_line_graph_expense(month:Optional[int|None]=None, db:AsyncSession=Depends(session.get_db)):
    return await income_expense._get_line_graph_month_expense(month=month, session=db)

@expense_income_handler.get('/get-line-graph-month-income')
async def get_line_graph_expense(month:Optional[int|None]=None, db:AsyncSession=Depends(session.get_db)):
    return await income_expense._get_line_graph_month_income(month=month, session=db)

@expense_income_handler.get('/get-line-graph-year-income')
async def get_line_graph_income(year:Optional[int|None]=None, db:AsyncSession=Depends(session.get_db)):
    return await income_expense._get_line_graph_year_income(year=year, session=db)

@expense_income_handler.get('/get-line-graph-year-expense')
async def get_line_graph_expense(year:Optional[int|None]=None, db:AsyncSession=Depends(session.get_db)):
    return await income_expense._get_line_graph_year_expense(year=year, session=db)

@expense_income_handler.get('/get-main-dashboard')
async def get_main_dashboard(db:AsyncSession=Depends(session.get_db)):
    return await income_expense._get_main_dashboard(session=db)

@expense_income_handler.get('/projects-done-bar-chart')
async def get_projects_done_chart(year:int=None, db:AsyncSession=Depends(session.get_db)):
    return await income_expense._get_projects_done_chart(session=db, year=year)

@expense_income_handler.get('/project-status-pie-chart')
async def get_project_status_pie_chart(db:AsyncSession=Depends(session.get_db)):
    return await income_expense._get_project_done_pie_chart(session=db)

