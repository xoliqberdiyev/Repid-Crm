from datetime import datetime
from fastapi import File, UploadFile, HTTPException
from typing import Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, delete, func, case, or_
from sqlalchemy.orm import joinedload, selectinload, Query

from database import models, schemas

from utils.hashing import Hasher


class EmployeeDal:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_employee(self, position_id):
        query = select(models.Employees).join(models.Position).where( 
                                                                     models.Employees.user_type!=models.UserType.super_admin).options(
                        selectinload(models.Employees.position))
        if position_id:
            query = select(models.Employees).join(models.Position).where(and_(
                                                                            models.Employees.position_id == position_id,
                                                                            models.Employees.user_type!=models.UserType.super_admin)).options(
                        selectinload(models.Employees.position))
        res = await self.db_session.execute(query)

        all_user = res.scalars().all()
        return all_user
    
    async def create_employee(self, first_name:str, last_name:str,
                              password:str, position_id: int,phone_number:str,
                              date_of_birth:datetime, date_of_jobstarted, salary:int,username:str,
                              image):
        
        new_employee = models.Employees(
            first_name=first_name,
            last_name=last_name,
            password=Hasher.get_password_hash(password),
            position_id=position_id,
            phone_number=phone_number,
            date_of_jobstarted=date_of_jobstarted,
            date_of_birth=date_of_birth,
            username=username,
            salary=salary,
            image=image
        )

        self.db_session.add(new_employee)
        await self.db_session.flush()

        query = (
        select(models.Employees)
        .options(joinedload(models.Employees.position))  
        .where(and_(models.Employees.id == new_employee.id), (models.Employees.is_active==True))
    )
        result = await self.db_session.execute(query)
        employee_with_position = result.scalars().first()

        return employee_with_position
    
    async def update_employee(self, first_name: str, last_name: str, user_id: int,
                          phone_number: str, date_of_birth: datetime,
                          date_of_jobstarted: datetime, salary: int, username: str,
                          image: str,position_id:int, is_active:bool):
        try:
            # Update the employee record
            query = (
                update(models.Employees)
                .where(and_(models.Employees.id == user_id))
                .values(
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    date_of_birth=date_of_birth,
                    salary=salary,
                    username=username,
                    is_active=is_active,
                    date_of_jobstarted=date_of_jobstarted,
                    image=image,
                    position_id=position_id
                )
                .returning(models.Employees)
            )
            user_update = await self.db_session.execute(query)
            await self.db_session.commit()  

            user_ = user_update.scalar_one_or_none()

            if not user_:
                raise NoResultFound(f"Active employee with ID {user_id} not found.")

            res_query = (
                select(models.Employees)
                .where(and_(models.Employees.id == user_.id))
                .join(models.Position)
                .options(joinedload(models.Employees.position))
            )
            result = await self.db_session.execute(res_query)
            updated_employee = result.scalar_one_or_none()

            if not updated_employee:
                raise NoResultFound(f"Unable to fetch updated employee with ID {user_id}.")

            return updated_employee

        except Exception as e:
            print(f"Error updating employee: {e}")
            raise

    async def get_username(self, username:str):
        query = (
            select(models.Employees).where(and_(models.Employees.username == username,models.Employees.is_active==True))
        )
        res = await self.db_session.execute(query)

        username = res.fetchone()
        if username is not None:
            return username[0]
        
    async def get_user_phone_number(self, phone_number:str):
        query = (
            select(models.Employees).where(and_(models.Employees.phone_number==phone_number,models.Employees.is_active==True))
        )
        res = await self.db_session.execute(query)

        return res.scalar_one_or_none()
        
    async def get_by_user_id(self, user_id):
        res = await self.db_session.execute(
            select(models.Employees).where(and_(models.Employees.id == user_id, models.Employees.is_active==True))
        )
        return res.fetchone()
    
    async def change_password(self,user_id, new_password):
        query = update(models.Employees).where(models.Employees.id==user_id).values(password=Hasher.get_password_hash(new_password)).returning(models.Employees)

        res = await self.db_session.execute(query)
        self.db_session.commit()

        return res.scalar_one_or_none()

    async def create_project(self, name:str, 
                            start_date:datetime,
                            end_date:datetime, 
                            image:str,
                            programmer_ids: list[str],
                            price: str):
        
        new_project = models.Project(
            name=name,
            start_date=start_date,
            end_date=end_date,
            image=image,
            price=price
        )
        self.db_session.add(new_project)
        await self.db_session.flush() 

        project_programmers = [
            models.ProjectProgrammer(
                project_id=new_project.id,
                programmer_id=int(programmer_id)
            )
            for programmer_id in programmer_ids
        ]
        self.db_session.add_all(project_programmers)

        await self.db_session.commit()

        return new_project
    
    async def get_programmers_by_project_id(self, project_id: int):
        result = await self.db_session.execute(
            select(models.Employees).join(models.ProjectProgrammer).where(and_(models.ProjectProgrammer.project_id == project_id),(models.Employees.is_active==True))
        )
        return result.scalars().all()

    async def get_all_projects(self, start_date, end_date, status):
        query = select(models.Project).where(models.Project.is_deleted==False)
        if (start_date and end_date) and status:
            query = select(models.Project).where(
                and_(
                    models.Project.is_deleted.is_(False),
                    models.Project.start_date.between(start_date, end_date),
                    models.Project.status == status
                )
            )
        elif start_date and end_date:
            query = select(models.Project).where(
                and_(
                    models.Project.is_deleted.is_(False),
                    models.Project.start_date.between(start_date, end_date),
                )
            )
        elif status:
            query = select(models.Project).where(
                and_(
                    models.Project.is_deleted.is_(False),
                    models.Project.status == status
                )
            )
        
        res = await self.db_session.execute(query)
        all_projects = res.scalars().all()

        return all_projects
        
    async def get_project_id(self, project_id):
        query = select(models.Project).where(and_(models.Project.is_deleted==False),(models.Project.id == project_id))
        res = await self.db_session.execute(query)
        all_projects = res.scalar_one_or_none()

        return all_projects

    async def get_employee_detail(self, user_id):
        query = select(models.Employees).where(and_(models.Employees.id==user_id),(models.Employees.is_active==True)).join(models.Position).options(selectinload(models.Employees.position))
        query_2 = (
            select(models.Project)
            .options(joinedload(models.Project.programmers)) 
            .where(and_(models.Project.programmers.any(models.Employees.id == user_id)),(models.Project.is_deleted==False))
        )
        result_user_info = await self.db_session.execute(query)
        result_user_projects = await self.db_session.execute(query_2)

        user_info = result_user_info.scalar_one()
        user_projects = result_user_projects.unique().scalars().all() 
        
        if user_info is None:
            raise HTTPException(status_code=404, detail="User not found")
        if user_info is not None and user_projects is not None:
            return (user_info, user_projects)

    async def create_operator(self,full_name:str, 
                              phone_number:str, 
                              description:str,operator_type_id:int):
        query = models.Operator(
            full_name=full_name,
            phone_number=phone_number,
            description=description,
            operator_type_id=operator_type_id,
        )

        self.db_session.add(query)
        await self.db_session.flush()  # Commit the session to persist the data
        # await self.db_session.refresh(query)  # Refresh to access relationships
        return query
    
    async def get_operator_type_by_id(self,op_id:int):
        query = (
            select(models.OperatorType)
            .where(models.OperatorType.id == op_id)
        )
        result = await self.db_session.execute(query)
        operator_with_type = result.scalar_one()
        return operator_with_type.name
    
    async def get_all_operator(self, oper_type_id:int,status:str):
        query = select(models.Operator).join(models.OperatorType).options(joinedload(models.Operator.operator_type))

        if oper_type_id and status:
            query = select(models.Operator).where(and_(models.Operator.operator_type_id == oper_type_id, models.Operator.status == status)).join(models.OperatorType).options(joinedload(models.Operator.operator_type))
        elif oper_type_id:
            query = select(models.Operator).where(models.Operator.operator_type_id == oper_type_id).join(models.OperatorType).options(joinedload(models.Operator.operator_type))
        elif status:
            query = select(models.Operator).where(models.Operator.status == status).join(models.OperatorType).options(joinedload(models.Operator.operator_type))

        res = await self.db_session.execute(query)

        return res.scalars().all()
    
    async def update_operator_by_type(self, oper_id, **kwargs):
        query = update(models.Operator).where(models.Operator.id==oper_id).values(kwargs).returning(models.Operator)
        res = await self.db_session.execute(query)
        await self.db_session.commit()

        res_oper = res.scalar_one_or_none()

        res_query = select(models.Operator).where(and_(models.Operator.id==res_oper.id)).join(models.OperatorType).options(joinedload(models.Operator.operator_type))
        res_ = await self.db_session.execute(res_query)

        return res_.scalar_one_or_none()

    async def delete_operator_by_type(self,oper_id):
        query = delete(models.Operator).where(models.Operator.id==oper_id)

        res = await self.db_session.execute(query)
        await self.db_session.commit()
        return True if res.rowcount >0 else False

    async def change_operator_status(self,oper_id:int, status:str):
        if status not in models.StatusOperator.__members__.values():
            raise ValueError(f"Invalid status: {status}. Must be one of {list(models.StatusOperator.__members__.values())}")
        
        try:
            status_enum = models.StatusOperator[status]  # Convert string to StatusOperator enum
        except KeyError:
            raise ValueError(f"Invalid status: {status}. Must be one of {list(models.StatusOperator.__members__.keys())}")

        query = (
            update(models.Operator)
            .values(status=status_enum)
            .filter_by(id = oper_id)
            .returning(models.Operator) 
        )

        res = await self.db_session.execute(query) 
  
        return res.scalar_one_or_none()

    async def delete_created_project(self, project_id:int):
        query = delete(models.Project).where(models.Project.id == project_id)

        res = await self.db_session.execute(query)
        self.db_session.commit()

        if res.rowcount > 0:
            return True
        return False

    async def update_created_project(self, project_id:int,image:str|None, body:schemas.UpdateProject):
    
        preject_update = (
                update(models.Project)
                .where(models.Project.id == project_id)
                .values(
                    name=body.name,
                    start_date=body.start_date,
                    end_date=body.end_date,
                    image=image,
                    price=body.price
                )
            ).returning(models.Project)
        res = await self.db_session.execute(preject_update)
        task_result = res.scalar_one_or_none()

        if not task_result:
            return None
        
        await self.db_session.execute(
            delete(models.ProjectProgrammer).where(models.ProjectProgrammer.project_id == project_id)
        )
        for programmer_id in body.programmers:
            project_programmer = models.ProjectProgrammer(
                project_id=project_id,
                programmer_id=programmer_id,
            )
            self.db_session.add(project_programmer)

            
        await self.db_session.commit()

        return task_result
    
    async def update_status_project(self, project_id:int, status:str):
        project_update = update(models.Project).where(models.Project.id == project_id).values(status=status).returning(models.Project)

        result = await self.db_session.execute(project_update)

        return result.scalar_one_or_none()
        
    async def get_list_position(self):
        query = select(models.Position)

        res = await self.db_session.execute(query)

        return res.scalars().all()
    
    async def create_position(self, name):
        query = models.Position(name=name)

        self.db_session.add(query)

        await self.db_session.commit()
        return query

    async def delete_employee(self, user_id):
        query = update(models.Employees).where(models.Employees.id==user_id).values(is_active=False)
        res = await self.db_session.execute(query)
        self.db_session.commit()

        if res.rowcount>0:
            return True
        return False
    
    async def get_employee_image(self,user_id: int):
        query = select(models.Employees.image).where(and_(models.Employees.id == user_id),(models.Employees.is_active==True)) 
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()