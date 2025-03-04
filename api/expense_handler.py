from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from fastapi_pagination.utils import disable_installed_extensions_check
from pydantic import ValidationError

from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession
from database import schemas, session, models
from api.action import expense_action
from api.login_handler import get_current_user_from_token

expense_handler = APIRouter()
           
@expense_handler.post('',description="Bu yerda shu status lar keladi (for_office, smm_service, other_expense, renting)")
async def create_expense(body:schemas.CreateNewExpence,db:AsyncSession=Depends(session.get_db),
                          current_user:models.Employees=Depends(get_current_user_from_token)):
    return await expense_action._create_expence_type(session=db, body=body)

@expense_handler.patch('',response_model=schemas.ShowExpenseType)
async def update_expense(update_params:schemas.UpdateExpenseByType, expense_id:int ,db:AsyncSession=Depends(session.get_db),
                          current_user:models.Employees=Depends(get_current_user_from_token)):
    try:
        body = update_params.model_dump(exclude_none=True)
        return await expense_action._update_expense_by_type(body=body, session=db, expense_id=expense_id)
    
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=f'Error occured:{e.errors()}'
        )

@expense_handler.get('', response_model = Page[schemas.ShowExpenseType],
                            description="Bu yerda shu status lar keladi (for_office, smm_service, other_expense,renting)"
                            "Agar filter qilganda (new,old) kiriting orderga iltimos Mavlon aka etibor bering",
                            )
async def get_list_expense_type(type:str, 
                                from_whom:str|None=None,
                                order:str='new',
                                db:AsyncSession=Depends(session.get_db),
                                start_date:datetime|None=None,
                                end_date:datetime|None=None,
                                 current_user:models.Employees=Depends(get_current_user_from_token),
                    ):
    expesne_types = await expense_action._get_expence_type_list(session=db, status=type,order=order,
                                                                start_date=start_date,end_date=end_date,
                                                                from_whom=from_whom)
    return paginate(expesne_types)

@expense_handler.delete('')
async def delete_given_expense(expense_id:int, db:AsyncSession=Depends(session.get_db),
                                current_user:models.Employees=Depends(get_current_user_from_token)):
    return await expense_action._delete_expense(session=db,expense_id=expense_id)

@expense_handler.post('/salary-employee',
                            description="Bu yerda faqat employee_id orqali user expense chiqadi")
async def create_expense_employee(body:schemas.CreatingExepnseEmployee, db:AsyncSession=Depends(session.get_db),
                                   current_user:models.Employees=Depends(get_current_user_from_token)):
    try:
        return await expense_action._create_expense_employee(session=db, body=body)
    except ValidationError as e:
        raise HTTPException(
            status_code=422, 
            detail=f'Error occored:{e.errors()}'
        )

@expense_handler.get('/salary-employee', response_model=Page[schemas.ShowExpenseEmployee])
async def get_list_expense_employee(
                                    order:str='new',
                                    db:AsyncSession=Depends(session.get_db),
                                    start_date:datetime|None=None,
                                    end_date:datetime|None=None,
                                     current_user:models.Employees=Depends(get_current_user_from_token)):
    user_expences = await expense_action._list_expense_employee(session=db, start_date=start_date, end_date=end_date,order=order)
    return paginate(user_expences)

@expense_handler.patch('/salary-employee')
async def update_expense_employee(income_employee_id:int,update_params: schemas.UpdateExpenseSalary,db:AsyncSession=Depends(session.get_db),
                                   current_user:models.Employees=Depends(get_current_user_from_token)):
    try:
        body = update_params.model_dump()
        return await expense_action._update_expense_employee(session=db, body=body,income_employee_id=income_employee_id)
    
    except ValidationError as e:
        raise HTTPException(
            status_code=422, 
            detail=f'Error occured:{e.errors()}'
        )

@expense_handler.get('/pie-chart')
async def get_expense_pie_chart(start_date:datetime|None = None, end_date:datetime|None=None,
                            db:AsyncSession=Depends(session.get_db),
                                 current_user:models.Employees=Depends(get_current_user_from_token)):
    return await expense_action._expense_pie_chart(session=db,start_date=start_date, end_date=end_date)

@expense_handler.get('/line-graph-month')
async def get_line_graph_expense(month:Optional[int|None]=None, year:Optional[int|None]=None,db:AsyncSession=Depends(session.get_db),
                                 current_user:models.Employees=Depends(get_current_user_from_token)):
    return await expense_action._get_line_graph_month_expense(month=month, session=db,year=year)


@expense_handler.get('/line-graph-year')
async def get_line_graph_expense(year:Optional[int|None]=None, db:AsyncSession=Depends(session.get_db),
                                 current_user:models.Employees=Depends(get_current_user_from_token)):
    return await expense_action._get_line_graph_year_expense(year=year, session=db)

@expense_handler.get('/main-dashboard')
async def get_main_dashboard(start_date:datetime|None = None, end_date:datetime|None=None,
                                db:AsyncSession=Depends(session.get_db),
                                current_user:models.Employees=Depends(get_current_user_from_token)):
    return await expense_action._get_main_dashboard(session=db, start_date=start_date, end_date=end_date)

@expense_handler.get('/projects-done-bar-chart')
async def get_projects_done_chart(year:int=None, db:AsyncSession=Depends(session.get_db),
                                  current_user:models.Employees=Depends(get_current_user_from_token)):
    return await expense_action._get_projects_done_chart(session=db, year=year)

@expense_handler.get('/project-status-pie-chart')
async def get_project_status_pie_chart(db:AsyncSession=Depends(session.get_db),
                                       current_user:models.Employees=Depends(get_current_user_from_token)):
    return await expense_action._get_project_done_pie_chart(session=db)