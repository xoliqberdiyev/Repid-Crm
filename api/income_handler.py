from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from fastapi_pagination.utils import disable_installed_extensions_check
from pydantic import ValidationError

from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession
from database import schemas, session, models
from api.action import income_action
from api.login_handler import get_current_user_from_token

income_router = APIRouter()

@income_router.post('/student-investor',description='Buyerda faqat qouvchilar va investordan kirim keladi (from_student, investor) kiriintg')
async def create_income_student(body:schemas.CreateIncomeStudent ,db:AsyncSession = Depends(session.get_db),
                                current_user:models.Employees=Depends(get_current_user_from_token)):
    try:
        return await income_action._create_income_student(body=body, session=db)
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=f'Error occured:{e.errors()}'
        )  

@income_router.get('/student-investor', response_model=Page[schemas.ShowIncomeStudent])
async def get_list_income_student(
                                type:str,
                                db:AsyncSession=Depends(session.get_db),
                                start_date:datetime|None=None,
                                end_date:datetime|None=None,
                                current_user:models.Employees=Depends(get_current_user_from_token)):
    income_students = await income_action._get_list_income_student(session=db,start_date=start_date,end_date=end_date,type=type)
    disable_installed_extensions_check()
    return paginate(income_students)

@income_router.delete('/student-investor')
async def delete_create_income(income_student_id:int, db:AsyncSession=Depends(session.get_db),
                               current_user:models.Employees=Depends(get_current_user_from_token)):
    return await income_action._delete_income_student(income_student_id=income_student_id, session=db)

@income_router.patch('/student-investor', response_model=schemas.ShowIncomeStudent)
async def update_income_student(income_student_id:int, update_params:schemas.UpdateStudentIncome, db:AsyncSession=Depends(session.get_db),
                                current_user:models.Employees=Depends(get_current_user_from_token)):
    body = update_params.model_dump(exclude_none=True)
    return await income_action._update_income_student(session=db, income_student_id=income_student_id,
                                                       body=body)

@income_router.post('/project', response_model=schemas.ShowIncomeProject)
async def create_income_project(body:schemas.CreateIncomeProject, db:AsyncSession=Depends(session.get_db),
                                current_user:models.Employees=Depends(get_current_user_from_token)):
    return await income_action._create_income_project(session=db, body=body)

@income_router.get('/project', response_model=Page[schemas.ShowIncomeProject])
async def get_list_income_project(db:AsyncSession=Depends(session.get_db),
                                  start_date:datetime|None=None,
                                  end_date:datetime|None=None,
                                  current_user:models.Employees=Depends(get_current_user_from_token)):
    income_projects = await income_action._get_list_income_project(session=db,start_date=start_date,end_date=end_date)
    return paginate(income_projects)

@income_router.delete('/project')
async def delete_income_project(income_project_id:int, db:AsyncSession=Depends(session.get_db),
                                current_user:models.Employees=Depends(get_current_user_from_token)):
    return await income_action._delete_income_project(income_project_id=income_project_id,
                                                       session=db)

@income_router.patch('/project')
async def update_income_project(income_project_id:int,update_params:schemas.UpdateIncomeProject,session:AsyncSession=Depends(session.get_db),
                                current_user:models.Employees=Depends(get_current_user_from_token)):
    try:
        body = update_params.model_dump()
        return await income_action._update_income_project(body=body,
                                                        session=session,
                                                        income_project_id=income_project_id)
    except ValidationError as e:

        raise HTTPException(
            status_code=422, 
            detail=f'Error occured:{e.errors()}'
        )

@income_router.get('/pie-chart')
async def get_income_chiechart(start_date:datetime|None=None, end_date:datetime|None=None,
                                db:AsyncSession=Depends(session.get_db),
                                current_user:models.Employees=Depends(get_current_user_from_token)):
    return await income_action._get_income_piechart(session=db, start_date=start_date, end_date=end_date)

@income_router.get('/line-graph-month')
async def get_line_graph_expense(month:Optional[int|None]=None, year:Optional[int|None]=None,
                                 db:AsyncSession=Depends(session.get_db),
                                 current_user:models.Employees=Depends(get_current_user_from_token)):
    return await income_action._get_line_graph_month_income(month=month, session=db,year=year)

@income_router.get('/line-graph-year')
async def get_line_graph_income(year:Optional[int|None]=None, db:AsyncSession=Depends(session.get_db),
                                current_user:models.Employees=Depends(get_current_user_from_token)):
    return await income_action._get_line_graph_year_income(year=year, session=db)
    
