import uvicorn
import logging

from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import Page, add_pagination, paginate

from api.employee_handler import emp_router
from api.income_expense_handler import expense_income_handler
from api.login_handler import login_user
from api.common_handler import common_router
from api.chat_handler import chat_handler

app = FastAPI(
    title="Repid CRM API",
    description="This is advanced api system in the world leading by google, meta and netflix",
    version="1.0.0",
    docs_url="/api/v1",  # Change the URL to "/api-docs"
    redoc_url="/redoc/api/v1",    # Optionally, change the URL for ReDoc documentation
    openapi_url="/openapi.json"
)
add_pagination(app)
main_api_router = APIRouter()
app.mount("/media", StaticFiles(directory="./media"), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. You can restrict to specific domains if needed.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


main_api_router.include_router(emp_router, prefix='/employee',tags=['employee'])
main_api_router.include_router(expense_income_handler, prefix='/income-expence',tags=['income_expence'])
main_api_router.include_router(login_user, prefix='/login', tags=['login'])
main_api_router.include_router(common_router, prefix='/common', tags=['common'])
main_api_router.include_router(chat_handler, prefix='/chat',tags=['chat'])

app.include_router(main_api_router)

@app.get('/ping')
async def checking_status():
    return {'status':True}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1',port=8000)
    

