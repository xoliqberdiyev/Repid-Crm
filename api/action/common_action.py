from fastapi import UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from typing import Optional

from database import models
from database import schemas
from dals import common_dal

async def _get_all_income_expected_value(session: AsyncSession):
    try:
        async with session.begin():
            com_dal = common_dal.CommonDal(session)

            all_income = await com_dal.get_income_expected_val()

            return [
                schemas.ShowExpectedValue(
                    id=income_val.id,
                    name=income_val.name,
                    date=income_val.date,
                    description=income_val.description,
                    type=income_val.type,
                    price=income_val.price
                )
                for income_val in all_income
            ]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _get_all_expense_expected_value(session: AsyncSession):
    try:
        async with session.begin():
            com_dal = common_dal.CommonDal(session)

            all_income = await com_dal.get_expence_expected_val()

            return [
                schemas.ShowExpectedValue(
                    id=income_val.id,
                    name=income_val.name,
                    date=income_val.date,
                    description=income_val.description,
                    type=income_val.type,
                    price=income_val.price,
                )
                for income_val in all_income
            ]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")
    
async def _create_expected_value(session:AsyncSession, body:schemas.CreateExpectedValue):
    try:
        async with session.begin():
            com_dal = common_dal.CommonDal(session)

            create_val = await com_dal.create_expected_val(body=body)

            return schemas.ShowExpectedValue(
                id=create_val.id,
                name=create_val.name,
                date=create_val.date,
                description=create_val.description,
                type=create_val.type,
                price=create_val.price
            )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")
    
async def _delete_expected_value(session:AsyncSession, expected_val_id:int):
    try:
        async with session.begin():
            com_dal = common_dal.CommonDal(session)

            delete_val = await com_dal.delete_expected_val(expected_val_id=expected_val_id)

            if delete_val:
                return {'succes':True,
                        'message':"Deleted successfully"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")
        
async def _update_expected_value(session:AsyncSession,expected_avl_id:int, body:dict):
    try:
        async with session.begin():
            com_dal = common_dal.CommonDal(session)

            update_val = await com_dal.update_expected_val(expected_avl_id=expected_avl_id, **body)

            if update_val:
                return {'succes':True,
                        'message':"Updated successfully"}
            return {'succes':False,
                        'message':"Error occured"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")
    
async def _create_new_task(session:AsyncSession, body:schemas.CreateNewTask,image_task:str):
        try:
            com_dal = common_dal.CommonDal(session)

            new_task = await com_dal.create_new_task(body=body, image_task=image_task)

            programmers = await com_dal.get_programmers_by_task_id(new_task.id)

            return schemas.ShowNewTask(
                id=new_task.id,
                name=new_task.name,
                image_task=f'https://crmm.repid.uz/media/tasks/{image_task}' if image_task != None else None,
                start_date=new_task.start_date,
                end_date=new_task.end_date,
                programmer_ids=[schemas.ProgrammerSchema.model_validate(programmer) for programmer in programmers],
                status=new_task.status,
                description=new_task.description
            )
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _get_all_tasks(current_user,
                         session: AsyncSession, 
                         task_id: Optional[int], status: Optional[str] = None):
    try:
        com_dal = common_dal.CommonDal(session)
        new_tasks = await com_dal.get_all_tasks(status=status, task_id=task_id)

        filtered_tasks = []
        for new_task in new_tasks:
            # Get programmers assigned to the task
            programmers = await com_dal.get_programmers_by_task_id(new_task.id)
            programmer_schemas = [schemas.ProgrammerSchema.model_validate(programmer) for programmer in programmers]
            
            # Check if current_user.id is in the assigned programmers
            if any(programmer.id == current_user.id for programmer in programmers) or (current_user.user_type == models.UserType.super_admin):
                filtered_tasks.append(schemas.ShowNewTask(
                    id=new_task.id,
                    name=new_task.name,
                    image_task=f'https://crmm.repid.uz/media/tasks/{new_task.image_task}' if new_task.image_task else None,
                    start_date=new_task.start_date,
                    end_date=new_task.end_date,
                    programmer_ids=programmer_schemas,
                    status=new_task.status,
                    description=new_task.description
                ))

        return filtered_tasks

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tasks: {str(e)}")

async def _delete_new_task_by_id(session:AsyncSession,task_id:int):
    try:
        async with session.begin():
            com_dal = common_dal.CommonDal(session)

            res = await com_dal.delete_new_task(task_id=task_id)

            if res:
                return {'success':True,
                        'message':'Task deleted successfully'}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _update_status_task(session:AsyncSession, task_id:int, status:str):
    try:
        async with session.begin():
            com_dal = common_dal.CommonDal(session)

            task_dal = await com_dal.update_status_task(status=status, task_id=task_id)

            if task_dal is not None:
                return {'success':True,
                        'message':'Muvafaqiyatli ozgardi'}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")
        
async def _update_new_task(session:AsyncSession, body:schemas.UpdateNewTask, task_id:int, image_task:str):
    try:

        com_dal = common_dal.CommonDal(session)

        task_update = await com_dal.update_new_task(task_id=task_id, body=body,image_task=image_task)

        programmers = await com_dal.get_programmers_by_task_id(task_update.id)

        if task_update:
            return schemas.ShowNewTask(
                id=task_update.id,
                name=task_update.name,
                image_task=f'https://crmm.repid.uz/media/tasks/{task_update.image_task}' if task_update.image_task != None else None,
                start_date=task_update.start_date,
                end_date=task_update.end_date,
                programmer_ids=[schemas.ProgrammerSchema.model_validate(programmer) for programmer in programmers],
                description=task_update.description,
                status=task_update.status
            )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _get_list_operator_type(session:AsyncSession):
    try:
        com_dal = common_dal.CommonDal(session)
        list_oper = await com_dal.get_list_oper_type()

        return [
            schemas.ShowPosition(
                id=oper_type.id,
                name=oper_type.name
            )
            for oper_type in list_oper
        ]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _create_operator_type(session:AsyncSession, name:str):
    try:
        async with session.begin():
            com_dal = common_dal.CommonDal(session)
            operator_type = await com_dal.create_operator_type(name=name)
            return schemas.ShowPosition(
                id=operator_type.id,
                name=operator_type.name
            )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _search_position_project(session:AsyncSession, query:str):
    try:
        async with session.begin():
            com_dal = common_dal.CommonDal(session)
            employyes, projects = await com_dal.search_query(query)

            return {
                'employes':employyes,
                'projects':projects
            }

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _create_login_password_note(session:AsyncSession, login:str, password:str, name:str):
    try:
        async with session.begin():
            com_dal = common_dal.CommonDal(session)
            login_password = await com_dal.create_login_password(name, login, password)

            return {
                'id':login_password.id,
                'name':login_password.name,
                'login':login_password.login,
                'password':login_password.password
            }

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _get_all_login_password(session:AsyncSession):
    try:
        async with session.begin():
            com_dal = common_dal.CommonDal(session)
            login_password = await com_dal.get_all_login_password_note()

            return [
                schemas.ShowLoginPassword(
                    id=login_note.id,
                    name=login_note.name,
                    login=login_note.login,
                    password=login_note.password
                )
                 for login_note in login_password
            ]

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _update_login_password_note(session:AsyncSession, body:dict,login_note_id:int):
    try:
        async with session.begin():
            com_dal = common_dal.CommonDal(session)
            login_password = await com_dal.update_login_password(login_note_id,**body)

            return schemas.ShowLoginPassword(
                id=login_password.id,
                name=login_password.name,
                login=login_password.login,
                password=login_password.password
            )

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")
    
async def _delete_login_password(session:AsyncSession, login_note_id:int):
    try:
        async with session.begin():
            com_dal = common_dal.CommonDal(session)
            login_password = await com_dal.delete_login_password(login_note_id)

            return {'success':True,
                    'message':'Deleted successfully'} if login_password else {'Success':False,
                                                                              'message':'Error happaend'}


    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _get_cash_income(session:AsyncSession):
    try:
        com_dal = common_dal.CommonDal(session)
        cash_income, cash_expense = await com_dal.get_cash_income()

        return {
            "total_income_cash":cash_income-cash_expense
        }

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")






