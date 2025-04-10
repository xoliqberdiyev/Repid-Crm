from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from database import schemas
from dals import user_dal

UPLOAD_USER = "uploads"
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
                image=f"https://crmm.repid.uz/media//{new_employee.image}" if new_employee.image else None,
                is_active=new_employee.is_active,
            )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _get_all_employee(session:AsyncSession, 
                            position_id:int,current_user:str,):
    try:
        async with session.begin():

            emp_dal = user_dal.EmployeeDal(session)
            all_users = await emp_dal.get_all_employee(position_id)  # Ensure this is an async call
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
                    image=f"https://crmm.repid.uz/media/uploads/{user.image}" if user.image else None,
                    is_active=user.is_active
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
                image=new_project.image,
                programmers=[schemas.ProgrammerSchema(id=programmer.id,
                                                      first_name=programmer.first_name,
                                                      last_name=programmer.last_name) for programmer in programmers]
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
    
async def _get_phone_number(session:AsyncSession, phone_number:str):
    async with session.begin():
        emp_dal = user_dal.EmployeeDal(session)

        user_phone_number = await emp_dal.get_user_phone_number(phone_number=phone_number)

        if user_phone_number is None:
            return False
        return user_phone_number
        
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
    
async def _change_user_password(sesion:AsyncSession, user_id:int, new_password:str):
    async with sesion.begin():
        com_dal = user_dal.EmployeeDal(sesion)

        new_user_password = await com_dal.change_password(user_id=user_id, new_password=new_password)

        if new_user_password is not None:
            return {'message':"User password changes successfully"}
 
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
                position_id=body.position_id,
                is_active=body.is_active,
                password=body.password,
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
                image=f"https://crmm.repid.uz/media/uploads/{new_employee.image}" if new_employee.image else None,
                is_active=new_employee.is_active
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

async def _get_image_by_user(session:AsyncSession, user_id:int):
    try:
        emp_dal = user_dal.EmployeeDal(session)

        user_image = await emp_dal.get_employee_image(user_id=user_id)

        return user_image
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

async def _create_chat_user(user1_id:int, user2_id:int,session:AsyncSession):
    emp_dal = user_dal.EmployeeDal(session)

    user_chat = await emp_dal.create_chat_user(user1_id=user1_id, user2_id=user2_id)

    return {
        'id':user_chat.id,
        'user1_id':user_chat.user1_id,
        'user2_id':user_chat.user2_id
    }

async def _start_messaging_create(data_chat:schemas.StartMessageCreate, sender_id:int, session:AsyncSession):
    emp_dal = user_dal.EmployeeDal(session)

    start_chat = await emp_dal.start_chat_create(data_chat=data_chat, sender_id=sender_id)

    return {
        'id':start_chat.id,
        'chat_id':start_chat.chat_id,
        'sender_id':start_chat.sender_id,
        'content':start_chat.content
    }

async def _chat_room_users(user_id:int, session:AsyncSession):
    emp_dal = user_dal.EmployeeDal(session)

    chat_rooms = await emp_dal.get_chat_rooms_user(user_id=user_id)

    data = [
        {"id":chat_room.id,
         "user1_id":chat_room.user1_id,
         "user2_id":chat_room.user2_id}

        for chat_room in chat_rooms
    ]

    return {"data":data}

async def _chat_room_messages(chat_room_id:int, session:AsyncSession):
    emp_dal = user_dal.EmployeeDal(session)

    chat_messages = await emp_dal.get_messages_chat_room(chat_room_id=chat_room_id)

    data = [
        {'id':chat_message.id,
         'sender_id':chat_message.sender_id,
         'content':chat_message.content,
         'created_at':chat_message.created_at
         }

        for chat_message in chat_messages
    ]

    return {'data':data}