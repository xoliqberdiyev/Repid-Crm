from typing import Optional, List
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_pagination import Page, paginate
from api.action import common_action
from database import schemas, session, models
from api.login_handler import get_current_user_from_token


common_router = APIRouter()


@common_router.get('/list-income-expected-val', response_model=Page[schemas.ShowExpectedValue])
async def get_all_income_val(db:AsyncSession = Depends(session.get_db), current_user:models.Employees=Depends(get_current_user_from_token)):
    expected_value =  await common_action._get_all_income_expected_value(session=db)
    return  paginate(expected_value)

@common_router.get('/list-expense-expected-val', response_model=Page[schemas.ShowExpectedValue])
async def get_all_income_val(db:AsyncSession = Depends(session.get_db),current_user:models.Employees=Depends(get_current_user_from_token)):
    expense_list =  await common_action._get_all_expense_expected_value(session=db)
    return paginate(expense_list)

@common_router.post('/create-expected-value', response_model=schemas.ShowExpectedValue)
async def get_all_income_val(body:schemas.CreateExpectedValue, db:AsyncSession = Depends(session.get_db),
                             current_user:models.Employees=Depends(get_current_user_from_token)):
    return await common_action._create_expected_value(session=db, body=body)

@common_router.delete('/delete-expected-val')
async def delete_expected_value(expected_val_id:int, db:AsyncSession = Depends(session.get_db),
                                current_user:models.Employees=Depends(get_current_user_from_token)):
    return await common_action._delete_expected_value(expected_val_id=expected_val_id, session=db)

@common_router.patch('/update-expected-val')
async def update_expected_value(expected_avl_id:int ,updated_val_params:schemas.UpdateExpectedValue, 
                                db:AsyncSession = Depends(session.get_db),
                                current_user:models.Employees=Depends(get_current_user_from_token)):
    body = updated_val_params.model_dump(exclude_none=True)
    return await common_action._update_expected_value(session=db, body=body, expected_avl_id=expected_avl_id)

@common_router.get('/get-all-new-task', response_model=List[schemas.ShowNewTask])
async def get_new_task(task_id:Optional[int]=None ,status:Optional[str]=None,db:AsyncSession = Depends(session.get_db),current_user:models.Employees=Depends(get_current_user_from_token)):
     return await common_action._get_all_tasks(status=status, session=db,task_id=task_id)
     
@common_router.get('/get-all-new-task', response_model=Page[schemas.ShowNewTask])
async def create_new_task(task_id:Optional[int]=None ,status:Optional[str]=None,db:AsyncSession = Depends(session.get_db),
                          current_user:models.Employees=Depends(get_current_user_from_token)):
    return await common_action._get_all_tasks(status=status, session=db,task_id=task_id)
  

@common_router.post('/create-new-task', response_model=schemas.ShowNewTask)
async def create_new_task(body:schemas.CreateNewTask, db:AsyncSession = Depends(session.get_db),
                          current_user:models.Employees=Depends(get_current_user_from_token)):
    return await common_action._create_new_task(body=body, session=db)

@common_router.delete('/delete-task')
async def delete_task_by_id(task_id:int, db:AsyncSession = Depends(session.get_db),
                            current_user:models.Employees=Depends(get_current_user_from_token)):
    return await common_action._delete_new_task_by_id(session=db, task_id=task_id)

@common_router.patch('/update_status_task')
async def update_task_status(task_id:int, status:str, db:AsyncSession = Depends(session.get_db),
                             current_user:models.Employees=Depends(get_current_user_from_token)):
    return await common_action._update_status_task(task_id=task_id, status=status, session=db)

@common_router.patch('/update_new_task')
async def update_task_status(task_id:int, update_new_task:schemas.UpdateNewTask, db:AsyncSession = Depends(session.get_db),
                             current_user:models.Employees=Depends(get_current_user_from_token)):
    body = update_new_task.model_dump(exclude_none=True)
    return await common_action._update_new_task(task_id=task_id,body=update_new_task, session=db)

@common_router.get('/list-operator-type', response_model=List[schemas.ShowPosition])
async def get_list_operator_type(db:AsyncSession = Depends(session.get_db),
                                 current_user:models.Employees=Depends(get_current_user_from_token)):
    return await common_action._get_list_operator_type(session=db)

@common_router.post('/create-operator-type',response_model=schemas.ShowPosition)
async def create_operator_type(name:str, db:AsyncSession=Depends(session.get_db),
                               current_user:models.Employees=Depends(get_current_user_from_token)):
    return await common_action._create_operator_type(session=db,name=name)

@common_router.get('/search')
async def search_position_project(query:str, db:AsyncSession=Depends(session.get_db),
                                  current_user:models.Employees=Depends(get_current_user_from_token)):
    return await common_action._search_position_project(query=query, session=db)
