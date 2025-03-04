import uvicorn

from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from api.employee_handler import emp_router
from api.login_handler import login_user
from api.common_handler import common_router
from api.chat_handler import chat_handler
from api.operator_handler import oper_router
from api.income_handler import income_router
from api.expense_handler import expense_handler

app = FastAPI(
    title="Repid CRM API",
    description="This is advanced api system in the world leading by google, meta and netflix",
    version="1.0.0",
    docs_url="/api/v1",  
    redoc_url="/redoc/api/v1",    
    openapi_url="/openapi.json"
)

main_api_router = APIRouter()
app.mount("/media", StaticFiles(directory="./media"), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

main_api_router.include_router(login_user, prefix='/login', tags=['login'])
main_api_router.include_router(emp_router, prefix='/employee',tags=['employee'])
main_api_router.include_router(expense_handler, prefix='/expence',tags=['expence'])
main_api_router.include_router(income_router, prefix='/income', tags=['income'])
main_api_router.include_router(common_router, prefix='/common', tags=['common'])
main_api_router.include_router(chat_handler, prefix='/chat',tags=['chat'])
main_api_router.include_router(oper_router, prefix='/operator', tags=['operator'])

app.include_router(main_api_router)
add_pagination(app)

@app.get('/ping')
async def checking_status():
    return {'status':True}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1',port=8000)