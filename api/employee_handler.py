from datetime import datetime, date
import shutil
import os

from typing import Optional, List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from fastapi_pagination import paginate
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError
from fastapi_pagination.utils import disable_installed_extensions_check

from api.action import employee
from api.login_handler import get_current_user_from_token
from database import schemas, session, models

emp_router = APIRouter()

UPLOAD_DIRECTORY = "media/uploads"  
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
UPLOAD_DIRECTORY1 = 'media/projects'

@emp_router.get('',response_model=Page[schemas.ShowEmployee])
async def get_all_employee(position_id:Optional[int]=None ,
                           db:AsyncSession = Depends(session.get_db),
                           current_user:models.Employees=Depends(get_current_user_from_token),
                            ):
    users = await employee._get_all_employee(db, position_id,current_user.username)
    disable_installed_extensions_check()
    return paginate(users)

@emp_router.delete('')
async def delete_employee(user_id:int, db:AsyncSession = Depends(session.get_db),
                          current_user:models.Employees=Depends(get_current_user_from_token)):
    return await employee._delete_employee(user_id=user_id, session=db)

@emp_router.post('', response_model=schemas.ShowEmployee)
async def create_employee(
    last_name: str|None = Form(default=None,examples=["Nimadir"]),
    first_name: str|None = Form(default=None, examples=['Kimdir']),
    username: str = Form(examples=['just_boy']),
    phone_number: str = Form(default=None,examples=['+998949252945']),
    password: str = Form(examples=['supersecure']),
    date_of_jobstarted: datetime = Form(examples=[date(2024,1,1)]),
    date_of_birth: Optional[datetime] = Form(default=None,examples=[date(2024,1,1)]),
    salary: int = Form(examples=[100000]),
    position_id: int = Form(examples=[1]),
    db: AsyncSession = Depends(session.get_db),
    file: Optional[UploadFile] = File(None),
    ):
    # current_user:models.Employees=Depends(get_current_user_from_token)
    if file:
        file_name = file.filename
        file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
    else:
        file_name = None

    try:
        
        employee_data = schemas.EmployeeCreate(
            date_of_birth=date_of_birth,
            salary=salary,
            position_id=position_id,
            last_name=last_name,
            username=username,
            first_name=first_name,
            phone_number=phone_number,
            password=password,
            date_of_jobstarted=date_of_jobstarted
        )
        return await employee._create_new_employee(body=employee_data, session=db, file_name=file_name)
    except ValidationError as e:
            raise HTTPException(
                status_code=422,
                detail=f"Validation error: {e.errors()}"
            )

@emp_router.patch('', response_model=schemas.ShowEmployee)
async def update_employee_detail(
    user_id:int,
    date_of_birth: Optional[datetime] = Form(default=None),
    salary: Optional[str] = Form(default=None),
    last_name: Optional[str] = Form(default=None),
    username: Optional[str] = Form(default=None),
    first_name: Optional[str] = Form(default=None),
    phone_number: Optional[str] = Form(default=None),
    date_of_jobstarted: Optional[datetime]= Form(default=None),
    db: AsyncSession = Depends(session.get_db),
    file: Optional[UploadFile] = File(None),
    image_remove: Optional[bool] = Form(default=False),
    position_id:Optional[int] = Form(default=None),
    is_active:Optional[bool] = Form(default=True),
    password:Optional[str] = Form(default=None),
    current_user:models.Employees=Depends(get_current_user_from_token)
):
    if file:  
        file_name = file.filename
        file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
    elif image_remove:  
        file_name = None
    else:
        # Keep the current image (don't change it)
        file_name = await employee._get_image_by_user(user_id=user_id, session=db)
        
    employee_data = schemas.UpdateEmployeeDetail(
        date_of_birth=date_of_birth,
        salary=salary,
        last_name=last_name,
        username=username,
        first_name=first_name,
        phone_number=phone_number,
        date_of_jobstarted=date_of_jobstarted,
        position_id=position_id,
        is_active=is_active,
        password=password
    )
    return await employee._update_employee_detail(session=db, body=employee_data,
                                                  image=file_name, user_id=user_id)

@emp_router.get('/detail', response_model=schemas.ShowEmployeeDetail)
async def get_detail_employee(user_id:int, db:AsyncSession = Depends(session.get_db),
                              current_user:models.Employees=Depends(get_current_user_from_token)):
    return await employee._get_detail_employee(user_id,db)

@emp_router.get('/projects', response_model=Page[schemas.ShowProject])
async def get_list_projects(start_date:datetime=None,
                            end_date:datetime=None,
                            status:str=None,
                            db:AsyncSession = Depends(session.get_db),
                            current_user:models.Employees=Depends(get_current_user_from_token),
                            ):
    projects =  await employee._get_all_projects(session=db, 
                                                 start_date=start_date, 
                                                 end_date=end_date,
                                                 status=status)
    
    disable_installed_extensions_check()
    return paginate(projects)

@emp_router.post('/project',response_model=schemas.ShowProject)
async def create_project(
    name: str = Form(examples=['Google']),
    start_date: datetime = Form(examples=[date(2024,1,1)]),
    end_date: datetime = Form(examples=[date(2024,1,1)]),
    price: str = Form(examples=['100000']),
    progemmer_list: list[str] = Form(examples=[["1","2"]]),
    image: Optional[UploadFile] = File(None),
    current_user:models.Employees=Depends(get_current_user_from_token),
    db: AsyncSession = Depends(session.get_db),
    ):
    try:
        programmer_ids = [int(x) for x in progemmer_list[0].split(',')]
    except ValueError:
        raise HTTPException(
                status_code=400, detail="All elements in progemmer_list must be valid integers."
            )
    if image != None:
        imagefile_name = image.filename
        try:
            file_path = os.path.join(UPLOAD_DIRECTORY1, image.filename)
            with open(file_path, 'wb') as buffer:
                shutil.copyfileobj(image.file, buffer)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error saving the file.")
    imagefile_name = None

    try:
        body = schemas.CreateProject(
            name=name,
            start_date=start_date,
            end_date=end_date,
            programmer_ids=programmer_ids,
            price=price
        )
    except ValidationError as e:
        raise HTTPException(
                status_code=422,
                detail=f"Validation error: {e.errors()[0]}"
            )

    return await employee._create_project(session=db, body=body,image=f'projects/{imagefile_name}')

@emp_router.delete('/project')
async def delete_created_project(project_id:int, db:AsyncSession = Depends(session.get_db),
                                 current_user:models.Employees=Depends(get_current_user_from_token)):
    return await employee._delete_created_project(session=db, project_id=project_id)

@emp_router.patch('/project', response_model=schemas.ShowProject)
async def update_created_project(project_id:int,
                                name: str = Form(examples=['Google']),
                                start_date: datetime = Form(examples=[date(2024,1,1)]),
                                end_date: datetime = Form(examples=[date(2024,1,1)]),
                                progemmer_list: list[str] = Form(examples=[["1","2"]]),
                                price: str = Form("1000000"),
                                image: Optional[UploadFile|None] = File(default=None),
                                db:AsyncSession = Depends(session.get_db),
                                current_user:models.Employees=Depends(get_current_user_from_token)):
    
    try:
        programmer_ids = [int(x) for x in progemmer_list[0].split(",") if x.isdigit()]
    except ValueError:
        raise HTTPException(
                status_code=400, detail="All elements in progemmer_list must be valid integers."
            )
    if image != None:
        image_filename = image.filename
        try:
            file_path = os.path.join(UPLOAD_DIRECTORY, image_filename)
            with open(file_path, 'wb') as buffer:
                shutil.copyfileobj(image_filename, buffer)
        except Exception as e:
                raise HTTPException(status_code=500, detail="Error saving the file.")
    image_filename = None
    try:
        body = schemas.UpdateProject(
            name=name,
            start_date=start_date,
            end_date=end_date,
            programmers=programmer_ids,
            price=price
        )
        return await employee._update_created_project(session=db,project_id=project_id, body=body,image=f'project/{image_filename}')
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=f'Error occured:{e.errors()}'
        )

@emp_router.patch('/project-status')
async def update_project_status(project_id:int, status:str, db:AsyncSession = Depends(session.get_db),
                                current_user:models.Employees=Depends(get_current_user_from_token)):
    return await employee._update_status_project(session=db, project_id=project_id, status=status)

@emp_router.get('/position', response_model=List[schemas.ShowPosition])
async def get_list_positions(db:AsyncSession = Depends(session.get_db),
                             current_user:models.Employees=Depends(get_current_user_from_token)
                            ):
    return await employee._get_list_position(session=db)

@emp_router.post('/position',response_model=schemas.ShowPosition)
async def create_position(name:str, db:AsyncSession = Depends(session.get_db),
                          current_user:models.Employees=Depends(get_current_user_from_token)):
    return await employee._create_position(session=db, name=name)

