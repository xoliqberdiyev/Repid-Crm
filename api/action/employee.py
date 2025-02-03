from fastapi import UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from typing import Optional
from database import schemas
from datetime import datetime
from dals import user_dal

import os


UPLOAD_USER = "uploalganda position ozgarish kerakds"
UPLOAD_PROJETC='projects'

async def _create_new_employee(body: schemas.EmployeeCreate, 
                               session: AsyncSession, 
                               file_name):
    try:
        async with session.begin():
            emp_dal = user_dal.EmployeeDal(session)
            if await emp_dal.get_username(body.username):
                raise HTTPException(status_code=422, detail='Username already exists')

            # Create a new employee via DAL
            new_employee = await emp_dal.create_employee(
                first_name=body.first_name,
                last_name=body.last_name,
                password=body.password,
                position_id=body.position_id,
                phone_number=body.phone_number,
                date_of_jobstarted=body.date_of_jobstarted,
                date_of_birth=body.date_of_birth,
                username=body.username,
                salary=body.salary,
                image=file_name
            )

            # Return the employee details
            return schemas.ShowEmployee(
                id=new_employee.id,
                last_name=new_employee.last_name,
                first_name=new_employee.first_name,
                phone_number=new_employee.phone_number,
                date_of_birth=new_employee.date_of_birth,
                position=new_employee.position.name,
                date_of_jobstarted=new_employee.date_of_jobstarted,
                username=new_employee.username,
                salary=new_employee.salary,
                user_type=new_employee.user_type,
                image=f"{UPLOAD_USER}/{new_employee.image}"
            )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _get_all_employee(session:AsyncSession, 
                            position_id:int,current_user:str,):
    try:
        async with session.begin():

            emp_dal = user_dal.EmployeeDal(session)
            all_users = await emp_dal.get_all_employee(position_id,current_user)  # Ensure this is an async call
            return [
                schemas.ShowEmployee(
                    id=user.id,
                    last_name=user.last_name,
                    first_name=user.first_name,
                    phone_number=user.phone_number,
                    date_of_birth=user.date_of_birth,
                    date_of_jobstarted=user.date_of_jobstarted,
                    username=user.username,
                    position=user.position.name,
                    salary=user.salary,
                    user_type=user.user_type,
                    image=f"{UPLOAD_USER}/{user.image}"
                )
                for user in all_users
            ]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")
    
async def _create_project(session:AsyncSession,
                          body:schemas.CreateProject,
                          image:str):
        try:
            emp_dal = user_dal.EmployeeDal(session)
            new_project = await emp_dal.create_project(name=body.name, 
                                                    start_date=body.start_date,
                                                    end_date=body.end_date,
                                                    price=body.price,
                                                    image=image, programmer_ids=body.programmer_ids)
            
            programmers = await emp_dal.get_programmers_by_project_id(new_project.id)

            return schemas.ShowProject(
                id=new_project.id,
                name=new_project.name,
                start_date=new_project.start_date,
                end_date=new_project.end_date,
                status=new_project.status,
                price=new_project.price,
                image=f"{UPLOAD_PROJETC}/{new_project.image}",
                programmers=[schemas.ProgrammerSchema.model_validate(programmer) for programmer in programmers]
            )
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _get_all_projects(session:AsyncSession, start_date, end_date, status):
    if start_date is None and end_date is None:
        pass
    elif start_date and end_date:
        pass
    elif start_date or end_date:
        raise HTTPException(status_code=402, detail="You must give me both date for projects")
    
    async with session.begin():
        try:
            emp_dal = user_dal.EmployeeDal(session)
            all_projects = await emp_dal.get_all_projects(start_date, end_date, status)

            return [
                schemas.ShowProject(
                    id=project.id,
                    name=project.name,
                    start_date=project.start_date,
                    end_date=project.end_date,
                    programmers=[schemas.ProgrammerSchema.model_validate(programmer) for programmer in await emp_dal.get_programmers_by_project_id(project.id)],
                    status=project.status,
                    price=project.price,
                    image=project.image,
                )
                
                for project in all_projects
            ]
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _get_detail_employee(user_id:int,
                               session:AsyncSession):
    try:
        async with session.begin():
            emp_dal = user_dal.EmployeeDal(session)
            if not await emp_dal.get_by_user_id(user_id=user_id):
                raise HTTPException(status_code=404, detail='User with this id is not found or not active')
            user_info, user_projects = await emp_dal.get_employee_detail(user_id=user_id)

            all_projects = [
                schemas.ShowProject(
                    id=project.id,
                    name=project.name,
                    start_date=project.start_date,
                    end_date=project.end_date,
                    programmers=[schemas.ProgrammerSchema.model_validate(programmer) for programmer in await emp_dal.get_programmers_by_project_id(project.id)],
                    status=project.status,
                    price=project.price,
                    image=project.image,
                )
                
                for project in user_projects
            ]
            

            return schemas.ShowEmployeeDetail(
                id=user_info.id,
                last_name=user_info.last_name,
                first_name=user_info.first_name,
                position_name=user_info.position.name,
                position_id=user_info.position.id,
                phone_number=user_info.phone_number,
                date_of_birth=user_info.date_of_birth,
                date_of_jobstarted=user_info.date_of_jobstarted,
                username=user_info.username,
                salary=user_info.salary,
                user_type=user_info.user_type,
                image=f"{UPLOAD_USER}/{user_info.image}",
                projects = all_projects
            )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _create_new_operatoe(session:AsyncSession, 
                               body:schemas.CreateOperator):
    try:
        async with session.begin():
            emp_dal = user_dal.EmployeeDal(session)
            oper_user = await emp_dal.create_operator(
                full_name=body.full_name,
                phone_number=body.phone_number,
                description=body.description,
                operator_type_id=body.operator_type_id
            )
            operator = await emp_dal.get_operator_type_by_id(oper_user.operator_type_id)

            return schemas.ShowOperator(
                id=oper_user.id,
                full_name=oper_user.full_name,
                phone_number=oper_user.phone_number,
                description=oper_user.description,
                operator_type_id= oper_user.operator_type_id,
                operator_type=operator,
                status=oper_user.status
            )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _get_all_operators(session:AsyncSession,
                                operator_type_id:int,
                                status:str):
    try:
        async with session.begin():
            emp_user = user_dal.EmployeeDal(session)
            operator_all = await emp_user.get_all_operator(oper_type_id=operator_type_id,status=status)

            return [
                schemas.ShowOperator(
                    id = oper_user.id,
                    full_name= oper_user.full_name,
                    phone_number = oper_user.phone_number,
                    description = oper_user.description,
                    operator_type_id = oper_user.operator_type_id,
                    operator_type = oper_user.operator_type.name,
                    status =  oper_user.status,
                    )
                    for oper_user in operator_all 
            ]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")
    
async def _change_operator_status(session:AsyncSession,
                                  oper_id:int,
                                  status:str):
    try:
        async with session.begin():
            dal_user = user_dal.EmployeeDal(session)
            change_status = await dal_user.change_operator_status(oper_id=oper_id,
                                                                status=status)
            if change_status:
                return {'success':True,
                        'message':'Muvafaqiyatli ozgartirildi'}
            
            return {'success':False,
                        'message':'Muvafaqiyatli ozgartirildi'}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _delete_created_project(session:AsyncSession, project_id:int):
    try:
        async with session.begin():
            emp_dal = user_dal.EmployeeDal(session)

            res = await emp_dal.delete_created_project(project_id=project_id)

            if res:
                return {'success':True,
                        'message':'Project deleted successfully'}
            return {'success':False,
                        'message':'Error occured'}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")
    
async def _update_created_project(session:AsyncSession, project_id:int, body:schemas.UpdateProject, image:str):
        try:
            emp_dal = user_dal.EmployeeDal(session)

            project_updated = await emp_dal.update_created_project(project_id=project_id, image=image, body=body)

            programmers = await emp_dal.get_programmers_by_project_id(project_updated.id)

            return schemas.ShowProject(
                id=project_updated.id,
                name=project_updated.name,
                start_date=project_updated.start_date,
                end_date=project_updated.end_date,
                status=project_updated.status,
                price=project_updated.price,
                image=project_updated.image,
                programmers=[schemas.ProgrammerSchema.model_validate(programmer) for programmer in programmers]
            )
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _update_status_project(session:AsyncSession, project_id:int, status:str):
    async with session.begin():
        emp_dal = user_dal.EmployeeDal(session)

        project_status = await emp_dal.update_status_project(project_id=project_id, status=status)

        if project_status:
            
            return {'success':True,
                    'message':'Status created successfully',
                    'status':project_status.status}
        return {'success':False,
                    'message':'Error occured'}
        
async def _get_list_position(session:AsyncSession):
    async with session.begin():
        emp_dal = user_dal.EmployeeDal(session)
        list_positions = await emp_dal.get_list_position()

        return [
            schemas.ShowPosition(
                id=position.id,
                name=position.name
            )
            for position in list_positions
        ]
    
async def _create_position(session:AsyncSession, name:str):
    async with session.begin():
        emp_dal = user_dal.EmployeeDal(session)
        position = await emp_dal.create_position(name=name)

        return schemas.ShowPosition(
            id=position.id,
            name=position.name
        )
    
async def _update_employee_detail(user_id:int, session:AsyncSession, body:schemas.UpdateEmployeeDetail,
                                  image:str):
        try:
            emp_dal = user_dal.EmployeeDal(session)

            # Create a new employee via DAL
            new_employee = await emp_dal.update_employee(
                first_name=body.first_name,
                last_name=body.last_name,
                phone_number=body.phone_number,
                date_of_jobstarted=body.date_of_jobstarted,
                date_of_birth=body.date_of_birth,
                username=body.username,
                salary=body.salary,
                image=image,
                user_id=user_id,
                position_id=body.position_id
            )

            # Return the employee details
            return schemas.ShowEmployee(
                id=new_employee.id,
                last_name=new_employee.last_name,
                first_name=new_employee.first_name,
                phone_number=new_employee.phone_number,
                date_of_birth=new_employee.date_of_birth,
                position=new_employee.position.name,
                date_of_jobstarted=new_employee.date_of_jobstarted,
                username=new_employee.username,
                salary=new_employee.salary,
                user_type=new_employee.user_type,
                image=f"{UPLOAD_USER}/{new_employee.image}"
            )
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")
    
async def _delete_employee(session:AsyncSession, user_id:int):
    try:
        async with session.begin():
            empl_dal = user_dal.EmployeeDal(session)

            delelted_user = await empl_dal.delete_employee(user_id=user_id)

            return {'success':True} if delelted_user else {'success':False}
    except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _update_operator(session:AsyncSession, oper_id:int, body:dict):
    try:
        emp_dal = user_dal.EmployeeDal(session)

        update_oper = await emp_dal.update_operator_by_type(oper_id=oper_id, **body)

        return schemas.ShowOperator(
                id = update_oper.id,
                full_name= update_oper.full_name,
                phone_number = update_oper.phone_number,
                description = update_oper.description,
                operator_type_id = update_oper.operator_type_id,
                operator_type = update_oper.operator_type.name,
                status =  update_oper.status,
                )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _delete_oper_by_id(session:AsyncSession, oper_id:int):
    try:
        empl_dal = user_dal.EmployeeDal(session)

        delete_user = await empl_dal.delete_operator_by_type(oper_id=oper_id)

        return {'success':True} if delete_user else {'success':False}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _get_image_by_user(session:AsyncSession, user_id:int):
    try:
        emp_dal = user_dal.EmployeeDal(session)

        user_image = await emp_dal.get_employee_image(user_id=user_id)

        return user_image
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")