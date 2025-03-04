from tests.conftest import create_test_auth_headers_for_user
from database.models import UserType
from datetime import date, datetime
import pytest
import json



class TestEmployeeAndPosition:
    async def create_test_user(self,create_user_in_database, create_position_from_database):
        position = await create_position_from_database("Backend")

        user_data = {
            "username": "test",
            "last_name": "test",
            "first_name": "test",
            "phone_number": "+345345345345",
            "salary": 100000,
            "position_id": position,
            "password": "testjkjk",
            "is_active": True,
            "user_type": UserType.admin,
            "date_of_birth": date(2024, 1, 1),
            "date_of_jobstarted": date(2024, 1, 1),
            "created_time": date(2024, 1, 1),
        }
        user_id = await create_user_in_database(**user_data)
        return (user_data,user_id)

    async def test_create_position(self, client, create_position_from_database, create_user_in_database):
        
        user_data = await self.create_test_user(create_user_in_database,create_position_from_database)

        resp = client.post(
            "/employee/position",
            headers=create_test_auth_headers_for_user(user_data[0]['username']),
            params={'name': 'Backend'}
        )

        data_from_resp = resp.json()
        assert resp.status_code == 200
        assert data_from_resp['name'] == "Backend"

    async def test_position_list(self,client,
                                 create_position_from_database,
                                 create_user_in_database):
        
        user_data = await self.create_test_user(create_user_in_database, create_position_from_database)

        resp = client.get('/employee/position',
                        headers=create_test_auth_headers_for_user(user_data[0]['username']))
        data_json = resp.json()
        assert resp.status_code==200
        assert data_json[0]['name'] == "Backend"

    async def test_employee_list(self, client, create_user_in_database, create_position_from_database):
        user_data = await self.create_test_user(create_user_in_database, create_position_from_database)
        user_data= user_data[0]

        resp = client.get('/employee',
                          headers=create_test_auth_headers_for_user(user_data['username']))
        data_json = resp.json()

        assert resp.status_code == 200
        assert data_json['items'][0]['username'] == user_data['username']
        assert data_json['items'][0]['last_name'] == user_data['last_name']
        assert data_json['items'][0]['first_name'] == user_data['first_name']
        assert data_json['items'][0]['phone_number'] == user_data['phone_number']
        assert data_json['items'][0]['salary'] == user_data['salary']
        assert data_json['items'][0]['is_active'] == user_data['is_active']
        assert data_json['items'][0]['user_type'] == user_data['user_type']
        assert data_json['items'][0]['date_of_birth'][:-9] == '2024-01-01'
        assert data_json['items'][0]['date_of_jobstarted'][:-9] == '2024-01-01'

    async def test_create_employee(self,client, create_user_in_database, create_position_from_database):
        user_data = await self.create_test_user(create_user_in_database, create_position_from_database)

        position = await create_position_from_database("Director")

        data_user = {
            "username": "test22",
            "last_name": "test",
            "first_name": "test",
            "phone_number": "+345345345345",
            "salary": '100000',
            "position_id": position,
            "password": "test2dgdbd",
            "date_of_birth": datetime(2024, 1, 1),
            "date_of_jobstarted": datetime(2024, 1, 1),
        }

        headers_ = create_test_auth_headers_for_user(user_data[0]['username'])
       

        resp = client.post('/employee',data=data_user,
                           headers =headers_)
        print(resp.json())
        
        data_json = resp.json()
        assert resp.status_code == 200
        assert data_json['username'] == data_user['username']
        assert data_json['last_name'] == data_user['last_name']
        assert data_json['first_name'] == data_user['first_name']
        assert data_json['phone_number'] == data_user['phone_number']
        assert data_json['salary'] == int(data_user['salary'])
        assert data_json['date_of_birth'][:-9] == '2024-01-01'
        assert data_json['date_of_jobstarted'][:-9] == '2024-01-01'
    
    async def test_delete_employee(self,client, create_user_in_database, create_position_from_database):
        user_data = await self.create_test_user(create_user_in_database, create_position_from_database)

        print(user_data)
        resp = client.delete('/employee',params={"user_id":user_data[1]},
                           headers =create_test_auth_headers_for_user(user_data[0]['username']))
        
        data_json = resp.json()
        assert resp.status_code == 200

    async def test_update_employee(self,client, create_user_in_database, create_position_from_database):
        user_data = await self.create_test_user(create_user_in_database, create_position_from_database)
        position = await create_position_from_database("Farrosh")

        data_user = {
            "username": "shaha",
            "last_name": "tosh",
            "first_name": "ploat",
            "phone_number": "+998949252945",
            "salary": '20000',
            "position_id": position,
            "date_of_birth": date(3004, 1, 1),
            "date_of_jobstarted": date(3004, 1, 1),
            "is_active":True
        }

        resp = client.patch('/employee', params={'user_id':user_data[1]},data=data_user,
                            headers=create_test_auth_headers_for_user(user_data[0]['username']))
        
        assert resp.status_code == 200
        data_json = resp.json()

        assert data_json['username'] == data_user['username']
        assert data_json['last_name'] == data_user['last_name']
        assert data_json['first_name'] == data_user['first_name']
        assert data_json['phone_number'] == data_user['phone_number']
        assert data_json['salary'] == 20000
        assert data_json['position'] == 'Farrosh'
        assert data_json['date_of_birth'][:-9] == '3004-01-01'
        assert data_json['is_active'] == data_user['is_active']